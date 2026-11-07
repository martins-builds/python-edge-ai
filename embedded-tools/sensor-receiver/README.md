# Sensor Stream Receiver

A command-line tool that reads framed IMU samples from a serial port (USB CDC on an STM32, or a simulated board), validates them, saves them to CSV with a metadata file, and optionally plots them live. It is the data collector for the Edge AI pipeline.

## Features

- Binary frame protocol with start byte and XOR checksum
- Resynchronises on the start byte after garbage or a mid-frame start
- Records timestamped samples to CSV, plus a JSON metadata file per session
- Optional live plot of ax, ay, az
- Reconnects automatically when the port disappears, and keeps writing to the same file
- Fake board for testing without hardware
- Tested on a real STM32F446RE over USB CDC

## Frame format

All multi-byte fields are little-endian. One frame is 18 bytes.

| Offset | Size | Field        | Type   | Notes                          |
|--------|------|--------------|--------|--------------------------------|
| 0      | 1    | start        | uint8  | always `0xAA`                  |
| 1      | 4    | timestamp_ms | uint32 | milliseconds                   |
| 5      | 2    | ax           | int16  | raw accelerometer              |
| 7      | 2    | ay           | int16  |                                |
| 9      | 2    | az           | int16  |                                |
| 11     | 2    | gx           | int16  | raw gyroscope                  |
| 13     | 2    | gy           | int16  |                                |
| 15     | 2    | gz           | int16  |                                |
| 17     | 1    | checksum     | uint8  | XOR of bytes 1 to 16 (payload) |

## Setup

```
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Usage

```
python record.py PORT --label LABEL [--baud 115200] [--plot] [--verbose]
```

| Argument    | Meaning                                              |
|-------------|------------------------------------------------------|
| `PORT`      | serial port, e.g. `/dev/tty.usbmodem1234561`         |
| `--label`   | activity label for the session (required)            |
| `--baud`    | baud rate (default 115200; ignored by USB CDC)       |
| `--plot`    | show a live plot of ax, ay, az                       |
| `--verbose` | show debug messages                                  |

Stop with Ctrl+C. The CSV and JSON are written either way.

### Without hardware (fake board)

Terminal 1:

```
python fake_board.py
```

Terminal 2:

```
python record.py /tmp/fakeboard --label test --plot
```

### With a real board

The firmware must send the frame format above. This was tested with an STM32F446RE (Nucleo-64) running a TinyUSB CDC firmware that sends one frame every 10 ms (100 Hz).

The Nucleo-64 has no user USB connector, so a data cable was wired to the pins:

| Cable wire | Signal | Nucleo pin |
|------------|--------|------------|
| Green      | D+     | PA12       |
| White      | D-     | PA11       |
| Red        | VBUS   | PA9 (VBUS sense input) |
| Black      | GND    | GND        |

The board's ST-Link USB connector stays plugged in for power and flashing.

Find the port by listing `ls /dev/tty.usbmodem*` before and after plugging in the data cable. The new entry is the board. Then:

```
python record.py /dev/tty.usbmodem1234561 --label hw_test --verbose
```

## Output

Each session creates two files in `data/`:

```
data/hw_test_20261107_090018.csv
data/hw_test_20261107_090018.json
```

The CSV has a header row (`timestamp_ms,ax,ay,az,gx,gy,gz`) and one row per sample.

The JSON records the session. This one is from the real board:

```json
{
  "label": "hw_test",
  "port": "/dev/tty.usbmodem1234561",
  "baud": 115200,
  "started": "2026-11-07T09:00:18",
  "duration_s": 31.9,
  "samples": 3185,
  "measured_rate_hz": 100.0,
  "csv": "hw_test_20261107_090018.csv"
}
```

`measured_rate_hz` is samples divided by duration, so it includes any time spent waiting for a reconnect.

## Project layout

```
sensor-receiver/
├── frame.py          Sample dataclass, encode, decode, checksum
├── receiver.py       read_frame(): resync and decode from a port
├── record.py         command-line tool: logging, CSV, metadata, plot, reconnect
├── fake_board.py     simulated board on a virtual serial port
├── loopback_demo.py  early demo using a loop:// port
└── receiver_demo.py  early demo of read_frame
```

## Known limitations

- The format is fixed: a timestamp plus six int16 IMU values. Another sensor needs a new `Sample` and `PAYLOAD_FMT` in `frame.py`.
- A stray `0xAA` byte directly before a real frame makes `read_frame` consume bytes from that frame, so one good frame can be lost. A buffer-based parser that re-scans from just after a false start would fix this.
- The live plot redraws every 5th sample, so it is a monitor, not a measurement tool.
- The firmware currently sends a test pattern (a wave on `ax`, constant `az`), not real IMU readings.

## Results

| Check                          | Result                                                  |
|--------------------------------|---------------------------------------------------------|
| Unit tests (kept locally)      | 10 passed; not included in this repository              |
| Fake board, measured rate      | about 82 Hz (board sleeps 10 ms per frame)              |
| Reconnect after board restart  | resumed in the same CSV, no crash                       |
| Real STM32F446RE over USB CDC  | 3185 samples in 31.9 s, measured rate 100.0 Hz          |

## What I would change

- Make the frame format configurable instead of hard-coded
- Replace the read-and-scan approach with a byte buffer to remove the false-start limitation
- Run the recorder and the plot in separate threads so plotting can never slow recording
- Check recorded timestamps for gaps over a longer real-board session (several minutes)
- Connect a real IMU to the firmware instead of the test pattern
