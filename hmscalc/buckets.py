"""Weekly and monthly aggregation buckets for dated duration records."""

from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass
from datetime import date
from typing import Iterable, Union

from .hms_datetime import HMSDateTime
from .hms_time import HMSTime

DurationInput = Union[HMSTime, str]
RecordInput = Union[HMSDateTime, tuple[date, DurationInput]]


@dataclass(frozen=True)
class BucketTotal:
    """Aggregated duration for one week or month."""

    period: str
    start: date
    total: HMSTime
    entry_count: int


def _normalize_record(record: RecordInput, *, strict: bool) -> tuple[date, HMSTime]:
    if isinstance(record, HMSDateTime):
        return record.day, record.time
    day, duration = record
    if isinstance(duration, str):
        return day, HMSTime(duration, strict=strict)
    return day, duration


def _week_label(day: date) -> tuple[str, date]:
    iso = day.isocalendar()
    period = f"{iso.year}-W{iso.week:02d}"
    start = date.fromisocalendar(iso.year, iso.week, 1)
    return period, start


def _month_label(day: date) -> tuple[str, date]:
    period = f"{day.year:04d}-{day.month:02d}"
    return period, date(day.year, day.month, 1)


def aggregate_by_week(
    records: Iterable[RecordInput],
    *,
    strict: bool = True,
) -> list[BucketTotal]:
    """Sum durations grouped by ISO week."""
    totals: dict[str, int] = defaultdict(int)
    counts: dict[str, int] = defaultdict(int)
    starts: dict[str, date] = {}

    for record in records:
        day, duration = _normalize_record(record, strict=strict)
        period, start = _week_label(day)
        totals[period] += duration.to_seconds()
        counts[period] += 1
        starts[period] = start

    return [
        BucketTotal(
            period=period,
            start=starts[period],
            total=HMSTime.from_seconds(totals[period]),
            entry_count=counts[period],
        )
        for period in sorted(starts, key=lambda key: starts[key])
    ]


def aggregate_by_month(
    records: Iterable[RecordInput],
    *,
    strict: bool = True,
) -> list[BucketTotal]:
    """Sum durations grouped by calendar month."""
    totals: dict[str, int] = defaultdict(int)
    counts: dict[str, int] = defaultdict(int)
    starts: dict[str, date] = {}

    for record in records:
        day, duration = _normalize_record(record, strict=strict)
        period, start = _month_label(day)
        totals[period] += duration.to_seconds()
        counts[period] += 1
        starts[period] = start

    return [
        BucketTotal(
            period=period,
            start=starts[period],
            total=HMSTime.from_seconds(totals[period]),
            entry_count=counts[period],
        )
        for period in sorted(starts, key=lambda key: starts[key])
    ]
