from dataclasses import dataclass
import struct
from functools import reduce
from operator import xor

@dataclass(frozen=True)
class Sample:
    timestamp_ms: int
    ax: int
    ay: int
    az: int
    gx: int
    gy: int
    gz: int

START = 0xAA
PAYLOAD_FMT = "<Ihhhhhh"
PAYLOAD_SIZE = struct.calcsize(PAYLOAD_FMT)   # 16
FRAME_SIZE = 1 + PAYLOAD_SIZE + 1             # 18

def checksum(payload: bytes) -> int:
    """XOR of every byte in the payload."""
    return reduce(xor, payload, 0)

def encode(sample: Sample) -> bytes:
    payload = struct.pack(PAYLOAD_FMT, sample.timestamp_ms, sample.ax, sample.ay, sample.az, sample.gx, sample.gy, sample.gz)
    return bytes([START]) + payload + bytes([checksum(payload)])

def decode(frame: bytes) -> Sample:
    if len(frame) != FRAME_SIZE:
        raise ValueError(f"expected {FRAME_SIZE} bytes, got {len(frame)}")                  # TODO: say what size you got
    if frame[0] != START:
        raise ValueError(...)                  # TODO
    payload = frame[1:-1]                      # skip the first and last byte
    if checksum(payload) != frame[-1]:
        raise ValueError(...)                  # TODO
    return Sample(*struct.unpack(PAYLOAD_FMT, payload))
