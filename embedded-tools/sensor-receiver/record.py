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
    print(args.port, args.baud, args.label)


if __name__ == "__main__":
    main()