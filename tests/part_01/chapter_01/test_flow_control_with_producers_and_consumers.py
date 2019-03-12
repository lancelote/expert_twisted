from twisted.internet.interfaces import IPushProducer
from twisted.internet.task import Clock
from twisted.trial import unittest
from zope.interface.verify import verifyObject

from src.part_01.chapter_01.flow_control_with_producers_and_consumers import StreamingProducer


class FakeConsumer(object):
    def __init__(self, written):
        self._written = written

    def write(self, data):
        self._written.append(data)


class TestsStreamingProducers(unittest.TestCase):
    def setUp(self):
        self.clock = Clock()
        self.written = []
        self.consumer = FakeConsumer(self.written)
        self.producer = StreamingProducer(self.clock, self.consumer)

    def test_providesIPushProducer(self):
        verifyObject(IPushProducer, self.producer)

    def test_resumeProducingSchedulesWrites(self):
        self.assertFalse(self.written)
        self.producer.resumeProducing()
        write_calls = len(self.written)
        self.clock.advance(self.producer.INTERVAL)
        new_write_calls = len(self.written)
        self.assertGreater(new_write_calls, write_calls)

    def test_pauseProducingStopsWrites(self):
        self.producer.resumeProducing()
        write_calls = len(self.written)
        self.producer.pauseProducing()
        self.clock.advance(self.producer.INTERVAL)
        self.assertEqual(len(self.written), write_calls)

    def test_stopProducingStopsWrites(self):
        self.producer.resumeProducing()
        write_calls = len(self.written)
        self.producer.stopProducing()
        self.clock.advance(self.producer.INTERVAL)
        self.assertEqual(len(self.written), write_calls)
