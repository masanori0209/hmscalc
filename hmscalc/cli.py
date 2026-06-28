"""Command-line interface for hmscalc."""

from __future__ import annotations

import argparse
import sys
from typing import Callable, Sequence

from hmscalc.hms_time import HMSTime

_AGGREGATORS: dict[str, Callable[[list[HMSTime]], HMSTime]] = {
    "add": HMSTime.sum,
    "sum": HMSTime.sum,
    "avg": HMSTime.average,
    "average": HMSTime.average,
    "min": HMSTime.min,
    "max": HMSTime.max,
}


def _parse_times(values: Sequence[str]) -> list[HMSTime]:
    return [HMSTime(value) for value in values]


def _read_times_from_stdin() -> list[str]:
    if sys.stdin.isatty():
        return []
    tokens: list[str] = []
    for line in sys.stdin.read().splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        tokens.extend(stripped.split())
    return tokens


def _subtract(times: list[HMSTime]) -> HMSTime:
    if len(times) < 2:
        raise ValueError("sub requires at least two time values")
    result = times[0]
    for other in times[1:]:
        result = result - other
    return result


def _format_result(result: HMSTime, fmt: str | None) -> str:
    if fmt is None:
        return str(result)
    return result.format(fmt)


def main(argv: list[str] | None = None) -> int:
    """Run the hmscalc CLI and return an exit code."""
    parser = argparse.ArgumentParser(
        prog="hmscalc",
        description="Add, subtract, and aggregate HH:MM[:SS] durations.",
    )
    parser.add_argument(
        "--format",
        choices=["HH:MM", "HH:MM:SS", "HH:MM:SS:PADDED"],
        help="Output format (default: HH:MM:SS)",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    for name, help_text in (
        ("add", "Add two or more durations"),
        ("sum", "Sum two or more durations (alias for add)"),
        ("avg", "Average of two or more durations"),
        ("min", "Minimum of two or more durations"),
        ("max", "Maximum of two or more durations"),
    ):
        cmd = subparsers.add_parser(name, help=help_text)
        cmd.add_argument(
            "times",
            nargs="*",
            metavar="TIME",
            help="HH:MM or HH:MM:SS (omit or use '-' to read from stdin)",
        )

    sub_parser = subparsers.add_parser("sub", help="Subtract durations (first minus the rest)")
    sub_parser.add_argument(
        "times",
        nargs="*",
        metavar="TIME",
        help="HH:MM or HH:MM:SS (omit or use '-' to read from stdin)",
    )

    args = parser.parse_args(argv)

    raw_times = list(args.times)
    if not raw_times or raw_times == ["-"]:
        raw_times = _read_times_from_stdin()
    if not raw_times:
        print("error: no time values provided", file=sys.stderr)
        return 1

    try:
        times = _parse_times(raw_times)
        if args.command == "sub":
            result = _subtract(times)
        else:
            aggregator = _AGGREGATORS[args.command]
            result = aggregator(times)
    except (TypeError, ValueError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
    except Exception as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1

    print(_format_result(result, args.format))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
