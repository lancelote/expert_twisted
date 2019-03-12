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
