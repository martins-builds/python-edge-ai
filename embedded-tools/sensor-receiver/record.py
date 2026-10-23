import argparse
import logging
import serial
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

    with serial.Serial(args.port, args.baud, timeout=1.0) as port, \
            csv_path.open("w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([fld.name for fld in fields(Sample)])
        log.info("recording to %s", csv_path)
        try:
            while True:
                sample = read_frame(port)
                if sample is None:
                    log.warning("no data for 1 s")
                    continue
                writer.writerow(astuple(sample))
                count += 1
                if count % 100 == 0:
                    log.info("%d samples", count)
        except KeyboardInterrupt:
            log.info("stopped, %d samples saved", count)

if __name__ == "__main__":
    main()