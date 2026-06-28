"""Tests for optional hmscalc.pandas_extra integration."""

from __future__ import annotations

from datetime import date

import pytest

pd = pytest.importorskip("pandas")

from hmscalc import HMSTime, pandas_extra


def test_parse_duration_series() -> None:
    """Test parsing a pandas Series to HMSTime objects."""
    series = pd.Series(["1:00", "2:30"])
    parsed = pandas_extra.parse_duration_series(series)
    assert parsed.iloc[0] == HMSTime("1:00")
    assert parsed.iloc[1] == HMSTime("2:30")


def test_aggregate_weekly_dataframe() -> None:
    """Test weekly aggregation from DataFrame."""
    df = pd.DataFrame(
        {
            "day": [date(2026, 6, 2), date(2026, 6, 3), date(2026, 6, 9)],
            "duration": ["1:00", "2:00", "0:30"],
        }
    )
    result = pandas_extra.aggregate_weekly(df, date_column="day", duration_column="duration")
    assert len(result) == 2
    assert result.iloc[0]["total"] == "3:00:00"
    assert result.iloc[0]["entry_count"] == 2


def test_aggregate_monthly_dataframe() -> None:
    """Test monthly aggregation from DataFrame."""
    df = pd.DataFrame(
        {
            "day": [date(2026, 6, 2), date(2026, 7, 1)],
            "duration": ["1:00", "2:00"],
        }
    )
    result = pandas_extra.aggregate_monthly(df, date_column="day", duration_column="duration")
    assert len(result) == 2
    assert list(result["period"]) == ["2026-06", "2026-07"]


def test_duration_series_to_strings() -> None:
    """Test converting HMSTime series back to strings."""
    series = pd.Series([HMSTime("1:00"), HMSTime("2:30:00")])
    strings = pandas_extra.duration_series_to_strings(series)
    assert strings.tolist() == ["1:00:00", "2:30:00"]
