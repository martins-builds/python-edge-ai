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
    frame = bytearray(encode(SAMPLE))
    frame[0] = 0x55
    with pytest.raises(ValueError, match="bad start byte"):
        decode(bytes(frame))


def test_corrupted_checksum_rejected():
    frame = bytearray(encode(SAMPLE))
    frame[5] ^= 0xFF
    with pytest.raises(ValueError, match="bad checksum"):
        decode(bytes(frame))


def test_out_of_range_rejected():
    with pytest.raises(ValueError, match="out of range"):
        encode(Sample(0, 40000, 0, 0, 0, 0, 0))