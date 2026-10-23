import argparse
import logging

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


if __name__ == "__main__":
    main()