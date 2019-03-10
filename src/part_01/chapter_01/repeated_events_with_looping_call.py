from twisted.internet import protocol, task
from twisted.internet.protocol import connectionDone


class HeartbeatProtocol(protocol.Protocol):

    def connectionMade(self):
        self._heartbeater = task.LoopingCall(self.transport.write, b'*')
        self._heartbeater.clock = self.factory._reactor
        self._heartbeater.start(interval=30.0)

    def connectionLost(self, reason=connectionDone):
        self._heartbeater.stop()


class HeartbeatProtocolFactory(protocol.Factory):
    protocol = HeartbeatProtocol

    def __init__(self, reactor):
        self._reactor = reactor
