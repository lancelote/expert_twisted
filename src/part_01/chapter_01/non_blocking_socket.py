import errno
import socket

listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
listener.bind(('127.0.0.1', 0))
listener.listen(1)
client = socket.create_connection(listener.getsockname())
server, _ = listener.accept()
client.setblocking(False)  # make non-blocking

try:
    while True:
        client.sendall(b'*'*1024)
except socket.error as e:
    # Instead of pausing the process sendall raises BlockingIOError
    assert e.errno == errno.EAGAIN  # OS reports: stop writing

server.setblocking(False)
try:
    while True:
        print(server.send(b'*'*1024))
except socket.error as e:
    # Send buffer is full
    print('terminated with EAGAIN', e.errno)
