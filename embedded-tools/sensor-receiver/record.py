from collections import deque
import matplotlib.pyplot as plt
import argparse
import logging
import serial
import json
import time
from receiver import read_frame

import csv
from dataclasses import astuple, fields
from datetime import datetime
from pathlib import Path

from frame import Sample

log = logging.getLogger("record")

def parse_args():
    parser = argparse.ArgumentParser(description="Record IMU frames from a serial port")
    parser.add_argument("port", help="serial port, e.g. /dev/cu.usbmodem1234")
    parser.add_argument("--baud", type=int, default=115200)
    parser.add_argument("--label", required=True, help="activity label for this session")
    parser.add_argument("--verbose", action="store_true", help="show debug messages")
    parser.add_argument("--plot", action="store_true", help="show a live plot of ax, ay, az")
    return parser.parse_args()


def main():
    args = parse_args()
    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.INFO,
        format="%(asctime)s %(levelname)s %(message)s",
    )
    log.info("port=%s baud=%d label=%s", args.port, args.baud, args.label)
    log.debug("this only shows with --verbose")
    out_dir = Path("data")
    out_dir.mkdir(exist_ok=True)
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    csv_path = out_dir / f"{args.label}_{stamp}.csv"
    count = 0

    N = 300
    if args.plot:
        plt.ion()
        fig, axis = plt.subplots()
        history = {name: deque([0] * N, maxlen=N) for name in ("ax", "ay", "az")}
        lines = {name: axis.plot(range(N), history[name], label=name)[0] for name in history}
        axis.set_ylim(-2000, 2000)
        axis.legend(loc="upper right")

    started = datetime.now()
    t0 = time.monotonic()

    with csv_path.open("w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([fld.name for fld in fields(Sample)])
        log.info("recording to %s", csv_path)
        try:
            while True:
                try:
                    with serial.Serial(args.port, args.baud, timeout=1.0) as port:
                        log.info("connected to %s", args.port)
                        while True:
                            sample = read_frame(port)
                            if sample is None:
                                log.warning("no data for 1 s")
                                continue
                            writer.writerow(astuple(sample))
                            count += 1
                            if count % 100 == 0:
                                log.info("%d samples", count)
                            if args.plot:
                                for name in history:
                                    history[name].append(getattr(sample, name))
                                if count % 5 == 0:
                                    for name, line in lines.items():
                                        line.set_ydata(history[name])
                                    plt.pause(0.001)
                except serial.SerialException as e:
                    log.warning("port lost (%s), retrying in 2 s", e)
                    time.sleep(2)
        except KeyboardInterrupt:
            log.info("stopped, %d samples saved", count)

    duration = time.monotonic() - t0
    meta = {
        "label": args.label,
        "port": args.port,
        "baud": args.baud,
        "started": started.isoformat(timespec="seconds"),
        "duration_s": round(duration, 1),
        "samples": count,
        "measured_rate_hz": round(count / duration, 1) if duration > 0 else 0,
        "csv": csv_path.name,
    }
    csv_path.with_suffix(".json").write_text(json.dumps(meta, indent=2))
    log.info("metadata saved to %s", csv_path.with_suffix(".json"))


if __name__ == "__main__":
    main()
    #working now.Would test on real board soon