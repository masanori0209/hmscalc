"""Optional pandas integration (requires ``pip install hmscalc[pandas]``)."""

from __future__ import annotations

from typing import TYPE_CHECKING, Iterable, Union

from .buckets import BucketTotal, RecordInput, aggregate_by_month, aggregate_by_week
from .hms_time import HMSTime

if TYPE_CHECKING:
    import pandas as pd


def _require_pandas() -> type[pd]:
    try:
        import pandas as pd
    except ImportError as exc:  # pragma: no cover - exercised via importorskip in tests
        raise ImportError(
            "pandas is required for this feature. Install with: pip install 'hmscalc[pandas]'"
        ) from exc
    return pd


def parse_duration_series(series: "pd.Series", *, strict: bool = True) -> "pd.Series":
    """Parse a string column into :class:`HMSTime` objects."""
    pd = _require_pandas()
    return series.map(lambda value: HMSTime(value, strict=strict)).astype(object)


def duration_series_to_strings(series: "pd.Series") -> "pd.Series":
    """Convert an HMSTime object column to ``HH:MM:SS`` strings."""
    _require_pandas()
    return series.map(lambda value: str(value))


def aggregate_weekly(
    df: "pd.DataFrame",
    *,
    date_column: str,
    duration_column: str,
    strict: bool = True,
) -> "pd.DataFrame":
    """Aggregate a DataFrame by ISO week using :func:`buckets.aggregate_by_week`."""
    pd = _require_pandas()
    records: Iterable[RecordInput] = (
        (row[date_column], row[duration_column]) for _, row in df.iterrows()
    )
    return bucket_totals_to_frame(aggregate_by_week(records, strict=strict))


def aggregate_monthly(
    df: "pd.DataFrame",
    *,
    date_column: str,
    duration_column: str,
    strict: bool = True,
) -> "pd.DataFrame":
    """Aggregate a DataFrame by calendar month using :func:`buckets.aggregate_by_month`."""
    pd = _require_pandas()
    records: Iterable[RecordInput] = (
        (row[date_column], row[duration_column]) for _, row in df.iterrows()
    )
    return bucket_totals_to_frame(aggregate_by_month(records, strict=strict))


def bucket_totals_to_frame(totals: Iterable[BucketTotal]) -> "pd.DataFrame":
    """Convert bucket totals to a pandas DataFrame."""
    pd = _require_pandas()
    rows = [
        {
            "period": bucket.period,
            "start": bucket.start,
            "total": str(bucket.total),
            "total_seconds": bucket.total.to_seconds(),
            "entry_count": bucket.entry_count,
        }
        for bucket in totals
    ]
    return pd.DataFrame(rows)
