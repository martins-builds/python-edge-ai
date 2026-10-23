import pytest
import serial
from frame import Sample, encode, FRAME_SIZE
from receiver import read_frame

SAMPLE = Sample(1000, 12, -3, 980, 1, -2, 3)


@pytest.fixture
def port():
    with serial.serial_for_url("loop://", timeout=0.1) as p:
        yield p


def test_reads_a_good_frame(port):
    port.write(encode(SAMPLE))
    assert read_frame(port) == SAMPLE


def test_skips_garbage_before_frame(port):
    port.write(b"\x01\x02\x03\x04\x05")
    port.write(encode(SAMPLE))
    assert read_frame(port) == SAMPLE


def test_empty_port_returns_none(port):
    assert read_frame(port) is None


def test_truncated_frame_returns_none():
    port.write(b"\x01\x02\x03\x04\x05\x06\x07\x08\x09\x10")
    encode(SAMPLE)[:10]
    assert read_frame(port) is None