"""Command-line interface for hmscalc."""

from __future__ import annotations

import argparse
import sys
from typing import Sequence

from hmscalc.hms_time import HMSTime


def _parse_times(values: Sequence[str]) -> list[HMSTime]:
    return [HMSTime(value) for value in values]


def _subtract(times: list[HMSTime]) -> HMSTime:
    if len(times) < 2:
        raise ValueError("sub requires at least two time values")
    result = times[0]
    for other in times[1:]:
        result = result - other
    return result


def main(argv: list[str] | None = None) -> int:
    """Run the hmscalc CLI and return an exit code."""
    parser = argparse.ArgumentParser(
        prog="hmscalc",
        description="Add, subtract, and aggregate HH:MM[:SS] durations.",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    add_parser = subparsers.add_parser("add", help="Add two or more durations")
    add_parser.add_argument("times", nargs="+", metavar="TIME", help="HH:MM or HH:MM:SS")

    sub_parser = subparsers.add_parser("sub", help="Subtract durations (first minus the rest)")
    sub_parser.add_argument("times", nargs="+", metavar="TIME", help="HH:MM or HH:MM:SS")

    sum_parser = subparsers.add_parser("sum", help="Sum two or more durations (alias for add)")
    sum_parser.add_argument("times", nargs="+", metavar="TIME", help="HH:MM or HH:MM:SS")

    args = parser.parse_args(argv)

    try:
        times = _parse_times(args.times)
        if args.command == "sub":
            result = _subtract(times)
        else:
            result = HMSTime.sum(times)
    except (TypeError, ValueError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
    except Exception as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1

    print(result)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
