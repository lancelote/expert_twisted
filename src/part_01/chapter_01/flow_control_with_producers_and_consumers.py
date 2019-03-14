from twisted.internet import protocol, reactor
from twisted.internet.interfaces import IPushProducer
from twisted.internet.task import LoopingCall
from zope.interface import implementer


@implementer(IPushProducer)
class StreamingProducer(object):
    INTERVAL = 0.001

    def __init__(self, reactor, consumer):
        self._data = [b'*', b'*']
        self._loop = LoopingCall(self._writeData, consumer.write)
        self._loop.clock = reactor

    def resumeProducing(self):
        print('resuming client producer')
        self._loop.start(self.INTERVAL)

    def pauseProducing(self):
        print('pausing client producer')
        self._loop.stop()

    def stopProducing(self):
        print('stopping client producer')
        if self._loop.running:
            self._loop.stop()

    def _writeData(self, write):
        print('client producer writing', len(self._data), 'bytes')
        write(b''.join(self._data))
        self._data.extend(self._data)


class StreamingClient(protocol.Protocol):
    def connectionMade(self):
        streaming_producer = StreamingProducer(self.factory._reactor, self.transport)
        self.transport.registerProducer(streaming_producer, True)
        streaming_producer.resumeProducing()


class ReceivingServer(protocol.Protocol):
    def dataReceived(self, data):
        print('server received', len(data), 'bytes')


class StreamingClientFactory(protocol.ClientFactory):
    protocol = StreamingClient

    def __init__(self, reactor):
        self._reactor = reactor


class ReceivingServerFactory(protocol.Factory):
    protocol = ReceivingServer


def main():
    listener = reactor.listenTCP(port=0, factory=ReceivingServerFactory(), interface='127.0.0.1')
    address = listener.getHost()
    reactor.connectTCP(host=address.host, port=address.port, factory=StreamingClientFactory(reactor))
    reactor.run()


if __name__ == '__main__':
    main()
