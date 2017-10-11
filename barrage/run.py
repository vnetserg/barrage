#!/usr/bin/env python3

import sys
import argparse

def run(TestCases):
    parser = argparse.ArgumentParser()
    parser.add_argument("app", help="compoiled executable to test")
    parser.add_argument("app_san", help="compiled executable with sanitizer")
    parser.add_argument("-s", "--seed", default=42, help="random seed", type=int)
    parser.add_argument("-f", "--forever", action="store_true", help="run forever")
    args = parser.parse_args()

    cases = TestCases(args.app, args.app_san, args.seed)
    try:
        if cases.run(args.forever):
            sys.exit(0)
        else:
            sys.exit(1)
    except KeyboardInterrupt:
        sys.exit(0)

if __name__ == "__main__":
    run()
