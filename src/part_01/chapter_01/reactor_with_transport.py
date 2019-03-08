import errno
import select
import socket
from abc import ABCMeta, abstractmethod


class Reactor(object):
    """Drives the program execution."""

    def __init__(self):
        self._readers = set()
        self._writers = set()

    def add_reader(self, transport):
        self._readers.add(transport)

    def add_writer(self, transport):
        self._writers.add(transport)

    def remove_reader(self, readable):
        self._readers.discard(readable)

    def remove_writer(self, writable):
        self._writers.discard(writable)

    def run(self):
        while self._readers or self._writers:
            r, w, _ = select.select(self._readers, self._writers, [])
            for readable in r:
                readable.do_read()
            for writable in w:
                if writable in self._writers:
                    writable.do_write()


class Protocol(object):
    """Application level handlers for socket events from transport."""

    __metaclass__ = ABCMeta

    @abstractmethod
    def make_connection(self, transport):
        pass

    @abstractmethod
    def data_received(self, data):
        pass

    @abstractmethod
    def connection_lost(self, exception_or_none):
        pass


class PingPongProtocol(Protocol):

    def __init__(self, identity, maximum=None):
        self._identity = identity
        self._received = 0
        self._maximum = maximum
        self.transport = None

    def make_connection(self, transport):
        self.transport = transport
        self.transport.write(b'*')  # begin sending data

    def data_received(self, data):
        self._received += len(data)
        print(self._identity, 'receives %s byte' % len(data))
        if self._maximum is not None and self._received >= self._maximum:
            print(self._identity, 'is closing the connection')
            self.transport.lose_connection()
        else:
            print(self._identity, 'sends a byte back')
            self.transport.write(b'*')

    def connection_lost(self, exception_or_none):
        print(self._identity, 'lost the connection:', exception_or_none)


class Transport(object):
    """Dispatching socket events."""

    def __init__(self, reactor, sock, protocol):
        self._reactor = reactor    # type: Reactor
        self._socket = sock        # type: socket.socket
        self._protocol = protocol  # type: Protocol
        self._buffer = b''
        self._on_completion = lambda: None

    def do_read(self):
        data = self._socket.recv(1024)
        if data:
            self._protocol.data_received(data)
        else:
            self._tear_down(None)

    def do_write(self):
        if self._buffer:
            try:
                written = self._socket.send(self._buffer)
            except socket.error as e:
                if e.errno != errno.EAGAIN:
                    self._tear_down(e)
                return
            else:
                print('transport wrote', written, 'bytes')
                self._buffer = self._buffer[written:]
        if not self._buffer:
            self._reactor.remove_writer(self)
            self._on_completion()

    # to work with select
    def fileno(self):
        return self._socket.fileno()

    def write(self, data):
        self._buffer += data
        self._reactor.add_writer(self)
        self.do_write()

    def lose_connection(self):
        if self._buffer:
            def complete():
                self._tear_down(None)
            self._on_completion = complete
        else:
            self._tear_down(None)

    def _tear_down(self, exception_or_none):
        self._reactor.remove_writer(self)
        self._reactor.remove_reader(self)
        self._socket.close()
        self._protocol.connection_lost(exception_or_none)

    def activate(self):
        self._socket.setblocking(False)
        self._protocol.make_connection(self)
        self._reactor.add_reader(self)
        self._reactor.add_writer(self)


class Listener(Transport):

    def activate(self):
        self._reactor.add_reader(self)

    def do_read(self):
        server, _ = self._socket.accept()
        protocol = PingPongProtocol('server')
        Transport(self._reactor, server, protocol).activate()


def main():
    listener_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    listener_sock.bind(('127.0.0.1', 0))
    listener_sock.listen(1)
    client_sock = socket.create_connection(listener_sock.getsockname())

    loop = Reactor()
    Listener(loop, listener_sock, None).activate()
    Transport(loop, client_sock, PingPongProtocol('client', maximum=100))\
        .activate()
    loop.run()


if __name__ == '__main__':
    main()
