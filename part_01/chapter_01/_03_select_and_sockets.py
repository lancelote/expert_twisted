import socket
import select

# Establish TCP connection
listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Internet TCP
listener.bind(('127.0.0.1', 0))  # random port
listener.listen(1)  # for 1 incoming connection

host, port = listener.getsockname()
client = socket.create_connection((host, port))

server, address = listener.accept()
print('connection from', address)

# Send test data
data = b'xyz'
client.sendall(data)
server.recv(1024)

server.sendall(data)
client.recv(1024)

# Using `select` to check socket events
#
# `select` receive:
#   - the list of sockets to check for readable events
#   - the list of sockets to check for writable events
#   - the list of sockets to check for exceptional events
#   - optional timeout

maybe_readable = [listener, client, server]
maybe_writable = [client, server]

readable, writable, _ = select.select(maybe_readable, maybe_writable, [], 0)
assert readable == []
assert writable == [client, server]

# Send some data from client to make server socket readable
client.sendall(b'xyz')
readable, writable, _ = select.select(maybe_readable, maybe_writable, [], 0)
assert readable == [server]
assert writable == [client, server]

assert server.recv(1024) == b'xyz'
readable, writable, _ = select.select(maybe_readable, maybe_writable, [], 0)
assert readable == []
assert writable == [client, server]
