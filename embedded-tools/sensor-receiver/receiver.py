import serial
from frame import Sample, decode, START, FRAME_SIZE


def read_frame(port: serial.Serial) -> Sample | None:
    """Return the next valid Sample, or None if the port times out."""
    while True:
        first = port.read(1)           # one byte at a time
        if not first:                  # empty bytes means timeout
            return None
        if first[0] != START:          # not a start byte: skip it
            continue
        rest = port.read(FRAME_SIZE - 1)
        if len(rest) != FRAME_SIZE - 1:    # timed out mid-frame
            return None
        try:
            return decode(first + rest)
        except ValueError:             # false start or bad checksum: keep scanning
            continue