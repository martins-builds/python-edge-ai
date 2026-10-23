import math
import os
import pty
import time
import serial
from receiver import read_frame

from frame import Sample, encode

master, slave = pty.openpty()
print("fake board on:", os.ttyname(slave))
link = "/tmp/fakeboard"
if os.path.islink(link):
    os.remove(link)
os.symlink(os.ttyname(slave), link)
print("also available as:", link)

t = 0
while True:
    s = Sample(t, int(1000 * math.sin(t / 300)), 0, 980, 0, 0, 0)
    os.write(master, encode(s))
    t += 10
    time.sleep(0.01)