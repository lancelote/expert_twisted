from twisted.internet import address
from twisted.trial import unittest
from twisted.test.proto_helpers import StringTransportWithDisconnection

from src.part_01.chapter_01.event_driven_twisted_program import PingPongClientFactory


class TestPingPongProtocol(unittest.SynchronousTestCase):
    def setUp(self):
        self.maximum = 100
        self.factory = PingPongClientFactory(self.maximum)
        self.protocol = self.factory.buildProtocol(address.IPv4Address('TCP', 'localhost', 1234))
        self.transport = StringTransportWithDisconnection()
        self.protocol.makeConnection(self.transport)
        self.transport.protocol = self.protocol

    def test_first_byte_written(self):
        self.assertEqual(len(self.transport.value()), 1)

    def test_byte_written_for_byte(self):
        self.protocol.dataReceived(b'*')
        self.assertEqual(len(self.transport.value()), 2)

    def test_receiving_maximum_loses_connection(self):
        self.protocol.dataReceived(b'*' * self.maximum)
        self.assertFalse(self.transport.connected)
