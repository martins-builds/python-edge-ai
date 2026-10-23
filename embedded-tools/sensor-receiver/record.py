import argparse
import logging
import serial
from receiver import read_frame

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
    with serial.Serial(args.port, args.baud, timeout=1.0) as port:
        log.info("connected")
        try:
            while True:
                sample = read_frame(port)
                if sample is None:
                    log.warning("no data for 1 s")
                    continue
                print(sample)
        except KeyboardInterrupt:
            log.info("stopped")

if __name__ == "__main__":
    main()