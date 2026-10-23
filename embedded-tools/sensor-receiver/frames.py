from dataclasses import dataclass
import struct
from functools import reduce
from operator import xor

START = 0xAA
PAYLOAD_FMT = "<Ihhhhhh"
PAYLOAD_SIZE = struct.calcsize(PAYLOAD_FMT)   # 16
FRAME_SIZE = 1 + PAYLOAD_SIZE + 1             # 18

@dataclass(frozen=True)
class Sample:
    timestamp_ms: int
    ax: int
    ay: int
    az: int
    gx: int
    gy: int
    gz: int

encode(sample: Sample) -> bytes
decode(frame: bytes) -> Sample
functools.reduce(operator.xor, payload)
decode(encode(s)) == s