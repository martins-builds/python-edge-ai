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
    try:
        payload = struct.pack(PAYLOAD_FMT, sample.timestamp_ms, sample.ax, sample.ay,
                              sample.az, sample.gx, sample.gy, sample.gz)
    except struct.error as e:
        raise ValueError(f"sample out of range: {sample}") from e
    return bytes([START]) + payload + bytes([checksum(payload)])

def decode(frame: bytes) -> Sample:
    if len(frame) != FRAME_SIZE:
        raise ValueError(f"expected {FRAME_SIZE} bytes, got {len(frame)}")
    if frame[0] != START:
        raise ValueError(f"bad start byte: expected 0x{START:02X}, got 0x{frame[0]:02X}")
    payload = frame[1:-1]
    if checksum(payload) != frame[-1]:
        raise ValueError(f"bad checksum: expected 0x{checksum(payload):02X}, got 0x{frame[-1]:02X}")
    return Sample(*struct.unpack(PAYLOAD_FMT, payload))
