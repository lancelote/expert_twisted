from twisted.trial import unittest
from twisted.internet import main, task, address
from twisted.test.proto_helpers import StringTransportWithDisconnection

from src.part_01.chapter_01.repeated_events_with_looping_call import HeartbeatProtocolFactory


class TestHeartbeatProtocol(unittest.SynchronousTestCase):

    def setUp(self):
        self.clock = task.Clock()
        self.factory = HeartbeatProtocolFactory(self.clock)
        self.protocol = self.factory.buildProtocol(address.IPv4Address('TCP', 'localhost', 1234))
        self.transport = StringTransportWithDisconnection()
        self.protocol.makeConnection(self.transport)
        self.transport.protocol = self.protocol

    def test_heartbeat_written(self):
        self.assertEqual(len(self.transport.value()), 1)
        self.clock.advance(60)
        self.assertEqual(len(self.transport.value()), 2)

    def test_lost_connection_stops_heartbeater(self):
        self.assertTrue(self.protocol._heartbeater.running)
        self.protocol.connectionLost(main.CONNECTION_DONE)
        self.assertFalse(self.protocol._heartbeater.running)
