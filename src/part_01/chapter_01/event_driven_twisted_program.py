from twisted.internet import protocol, reactor
from twisted.internet.protocol import connectionDone


class PingPongProtocol(protocol.Protocol):

    def __init__(self):
        self.received = 0

    def connectionMade(self):
        """Event handler called when connection is ready."""
        self.transport.write(b'*')

    def dataReceived(self, data):
        self.received += len(data)
        if self.factory.maximum is not None and self.received >= self.factory.maximum:
            print(self.factory.identity, 'is closing the connection')
            self.transport.loseConnection()
        else:
            self.transport.write(b'*')
            print(self.factory.identity, 'wrote a byte')

    def connectionLost(self, reason=connectionDone):
        print(self.factory.identity, 'lost the connection:', reason)


class PingPongServerFactory(protocol.Factory):
    protocol = PingPongProtocol
    identity = 'Server'

    def __init__(self, maximum=None):
        self.maximum = maximum


class PingPongClientFactory(protocol.ClientFactory):
    protocol = PingPongProtocol
    identity = 'Client'

    def __init__(self, maximum=None):
        self.maximum = maximum


def main():
    listener = reactor.listenTCP(port=0, factory=PingPongServerFactory(), interface='127.0.0.1')
    address = listener.getHost()
    reactor.connectTCP(host=address.host, port=address.port, factory=PingPongClientFactory(maximum=100))
    reactor.run()


if __name__ == '__main__':
    main()
