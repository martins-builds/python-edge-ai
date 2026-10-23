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