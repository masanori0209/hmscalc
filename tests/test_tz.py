"""Tests for hmscalc.tz."""

from __future__ import annotations

from datetime import date, datetime, timezone
from zoneinfo import ZoneInfo

import pytest

from hmscalc import tz


def test_parse_datetime_with_timezone() -> None:
    """Test parsing attaches timezone without shifting clock time."""
    dt = tz.parse_datetime("2026-06-28 09:00", tz="Asia/Tokyo")
    assert dt.tzinfo == ZoneInfo("Asia/Tokyo")
    assert dt.hour == 9
    assert dt.minute == 0


def test_localize_naive() -> None:
    """Test localize attaches tz to naive datetime."""
    naive = datetime(2026, 6, 28, 9, 0)
    aware = tz.localize(naive, "Asia/Tokyo")
    assert aware.tzinfo == ZoneInfo("Asia/Tokyo")
    assert aware.hour == 9


def test_localize_already_aware_raises() -> None:
    """Test localize rejects aware datetimes."""
    aware = datetime(2026, 6, 28, 9, 0, tzinfo=timezone.utc)
    with pytest.raises(ValueError, match="already timezone-aware"):
        tz.localize(aware, "Asia/Tokyo")


def test_to_timezone_converts() -> None:
    """Test conversion between timezones."""
    tokyo = tz.localize(datetime(2026, 6, 28, 9, 0), "Asia/Tokyo")
    utc = tz.to_timezone(tokyo, "UTC")
    assert utc.hour == 0  # JST is UTC+9


def test_local_to_utc() -> None:
    """Test local_to_utc helper."""
    tokyo = tz.localize(datetime(2026, 6, 28, 9, 0), "Asia/Tokyo")
    assert tz.local_to_utc(tokyo).tzinfo == timezone.utc


def test_daily_window() -> None:
    """Test daily working window is timezone-aware."""
    start, end = tz.daily_window(date(2026, 6, 28), "9:00", "18:00", "Asia/Tokyo")
    assert start.tzinfo == ZoneInfo("Asia/Tokyo")
    assert end.tzinfo == ZoneInfo("Asia/Tokyo")
    assert start.hour == 9
    assert end.hour == 18


def test_time_on_date_with_hms_string() -> None:
    """Test HMSTime strings work for daily bounds."""
    dt = tz.time_on_date(date(2026, 6, 28), "1:30", "Asia/Tokyo")
    assert dt.hour == 1
    assert dt.minute == 30
