import select
import socket

DATA = [b'*', b'*']


# Reactor -> reacts on socket events
class Reactor(object):
    def __init__(self):
        self._readers = {}
        self._writers = {}

    def add_reader(self, readable, handler):
        self._readers[readable] = handler

    def add_writer(self, writable, handler):
        self._writers[writable] = handler

    def remove_reader(self, readable):
        self._readers.pop(readable, None)

    def remove_writer(self, writable):
        self._writers.pop(writable, None)

    @property
    def readers(self):
        return list(self._readers)

    @property
    def writers(self):
        return list(self._writers)

    def run(self):
        while self._readers or self._writers:
            r, w, _ = select.select(self.readers, self.writers, [])
            for readable in r:
                self._readers[readable](self, readable)
            for writable in w:
                # connection may be already closed as a read event
                if writable in self._writers:
                    self._writers[writable](self, writable)


def accept(reactor, listener):
    server, _ = listener.accept()
    reactor.add_reader(server, read)


def read(reactor, sock):
    data = sock.recv(1024)
    if data:
        print('server received', len(data), 'bytes')
    else:
        sock.close()
        print('server closed')
        reactor.remove_reader(sock)


def write(_, sock):
    sock.sendall(b''.join(DATA))
    print('client send', len(DATA), 'bytes')
    # double the amount of data to simulate real network application
    DATA.extend(DATA)


def main():
    listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    listener.bind(('127.0.0.1', 0))
    listener.listen(1)
    client = socket.create_connection(listener.getsockname())

    loop = Reactor()
    loop.add_writer(client, write)
    loop.add_reader(listener, accept)
    loop.run()


if __name__ == '__main__':
    main()
