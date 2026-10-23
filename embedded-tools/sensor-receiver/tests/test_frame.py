import pytest
from frame import Sample, encode, decode, FRAME_SIZE

SAMPLE = Sample(timestamp_ms=1000, ax=12, ay=-3, az=980, gx=1, gy=-2, gz=3)


def test_round_trip():
    assert decode(encode(SAMPLE)) == SAMPLE


def test_frame_size():
    assert len(encode(SAMPLE)) == FRAME_SIZE


def test_short_frame_rejected():
    with pytest.raises(ValueError, match="expected 18 bytes"):
        decode(encode(SAMPLE)[:-1])


def test_bad_start_byte_rejected():
    match="bad start byte"
def test_corrupted_checksum_rejected():
    match="bad checksum"