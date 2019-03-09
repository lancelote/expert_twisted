import errno
import socket

from src.part_01.chapter_01.event_loop_around_select import Reactor, accept

DATA = [b'*', b'*']


class BufferWrites(object):
    """Transport."""

    def __init__(self, data_to_write, on_completion):
        self._buffer = data_to_write
        self._on_completion = on_completion

    def buffering_write(self, reactor, sock):
        if self._buffer:
            try:
                written = sock.send(self._buffer)
            except socket.error as e:
                if e.errno != errno.EAGAIN:
                    raise  # unexpected error
                print('EAGAIN was raised')
                return
            else:
                print('wrote', written, 'bytes')
                self._buffer = self._buffer[written:]
        if not self._buffer:
            reactor.remove_writer(sock)
            self._on_completion(reactor, sock)


def write(reactor, sock):
    writer = BufferWrites(b''.join(DATA), on_completion=write)
    reactor.add_writer(sock, writer.buffering_write)
    print('client buffering', len(DATA), 'bytes to write')
    DATA.extend(DATA)


def main():
    listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    listener.bind(('127.0.0.1', 0))
    listener.listen(1)
    client = socket.create_connection(listener.getsockname())
    client.setblocking(False)

    loop = Reactor()
    loop.add_writer(client, write)
    loop.add_reader(listener, accept)
    loop.run()
    # Will fail with a MemoryError


if __name__ == '__main__':
    main()
