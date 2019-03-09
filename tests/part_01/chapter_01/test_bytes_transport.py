from twisted.trial import unittest

from src.part_01.chapter_01.bytes_transport import BytesTransport
from src.part_01.chapter_01.reactor_with_transport import PingPongProtocol


class TestPingPongProtocol(unittest.TestCase):

    def setUp(self):
        self.maximum = 100
        self.protocol = PingPongProtocol('client', maximum=self.maximum)
        self.transport = BytesTransport(self.protocol)
        self.protocol.make_connection(self.transport)

    def test_first_byte_written(self):
        self.assertEqual(len(self.transport.output.getvalue()), 1)

    def test_byte_written_for_byte(self):
        self.protocol.data_received(b'*')
        self.assertEqual(len(self.transport.output.getvalue()), 2)

    def test_receiving_maximum_loses_connection(self):
        self.protocol.data_received(b'*' * self.maximum)
        self.assertTrue(self.transport.output.closed)
