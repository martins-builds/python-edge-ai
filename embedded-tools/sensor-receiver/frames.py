from dataclasses import dataclass

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
ecode(frame: bytes) -> Sample
functools.reduce(operator.xor, payload)
decode(encode(s)) == s