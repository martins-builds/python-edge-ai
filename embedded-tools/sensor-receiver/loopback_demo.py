import serial
from frame import Sample, encode, decode, FRAME_SIZE

samples = [
    Sample(1000, 12, -3, 980, 1, -2, 3),
    Sample(1010, 14, -2, 978, 0, -1, 4),
    Sample(1020, 11, -4, 981, 2, -3, 2),
    Sample(1030, 13, -2, 984, 1, -2, 4),
]

with serial.serial_for_url("loop://", timeout=1.0) as port:
    port.write(b"\x01\x02\x03\x04\x05")
    for s in samples:
        port.write(encode(s))

    for _ in range(len(samples)):
        frame = port.read(FRAME_SIZE)
        print(decode(frame))