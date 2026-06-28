"""Tests for hmscalc.buckets weekly/monthly aggregation."""

from __future__ import annotations

from datetime import date

from hmscalc import HMSDateTime, HMSTime, buckets


def test_aggregate_by_week() -> None:
    """Test ISO week grouping."""
    records = [
        (date(2026, 6, 2), "1:00"),
        (date(2026, 6, 3), "2:00"),
        (date(2026, 6, 9), "0:30"),
    ]
    totals = buckets.aggregate_by_week(records)
    assert len(totals) == 2
    assert totals[0].entry_count == 2
    assert totals[0].total == HMSTime("3:00:00")
    assert totals[1].total == HMSTime("0:30:00")
    assert totals[0].period.startswith("2026-W")


def test_aggregate_by_month() -> None:
    """Test calendar month grouping."""
    records = [
        (date(2026, 6, 2), "1:00"),
        (date(2026, 6, 28), "2:00"),
        (date(2026, 7, 1), "0:30"),
    ]
    totals = buckets.aggregate_by_month(records)
    assert len(totals) == 2
    assert totals[0].period == "2026-06"
    assert totals[0].total == HMSTime("3:00:00")
    assert totals[1].period == "2026-07"


def test_hms_datetime_records() -> None:
    """Test HMSDateTime records aggregate correctly."""
    records = [HMSDateTime.from_strings("2026-06-02", "1:00")]
    totals = buckets.aggregate_by_week(records)
    assert totals[0].entry_count == 1


def test_lenient_duration_strings() -> None:
    """Test lenient parsing in bucket aggregation."""
    records = [(date(2026, 6, 2), "1:90")]
    totals = buckets.aggregate_by_week(records, strict=False)
    assert totals[0].total == HMSTime("2:30:00")


def test_hms_time_duration_objects() -> None:
    """Test tuple records with HMSTime objects."""
    records = [(date(2026, 6, 2), HMSTime("1:30"))]
    totals = buckets.aggregate_by_month(records)
    assert totals[0].total == HMSTime("1:30:00")
