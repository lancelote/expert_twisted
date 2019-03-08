import pytest

from src.part_01.chapter_01.bytes_transport import BytesTransport
from src.part_01.chapter_01.reactor_with_transport import PingPongProtocol

MAXIMUM = 100


@pytest.fixture
def protocol():
    return PingPongProtocol('client', maximum=MAXIMUM)


@pytest.fixture
def transport(protocol):
    bytes_transport = BytesTransport(protocol)
    protocol.make_connection(bytes_transport)
    return bytes_transport


def test_first_bytes_written(transport):
    assert len(transport.output.getvalue()) == 1


def test_byte_written_for_byte(protocol, transport):
    protocol.data_received(b'*')
    assert len(transport.output.getvalue()) == 2


def test_receiving_maximum_loses_connection(protocol, transport):
    protocol.data_received(b'*' * MAXIMUM)
    assert transport.output.closed
