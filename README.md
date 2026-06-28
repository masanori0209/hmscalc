# hmscalc

[![PyPI version](https://img.shields.io/pypi/v/hmscalc.svg)](https://pypi.org/project/hmscalc/)
[![Stable](https://img.shields.io/badge/status-stable-green.svg)](docs/API_STABILITY.md)
[![Python versions](https://img.shields.io/pypi/pyversions/hmscalc.svg)](https://pypi.org/project/hmscalc/)
[![CI](https://github.com/masanori0209/hmscalc/actions/workflows/test.yml/badge.svg)](https://github.com/masanori0209/hmscalc/actions/workflows/test.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Add and subtract **HH:MM** / **HH:MM:SS** time strings in Python — no manual conversion to seconds required.

**Stable since v1.0.0** (latest: **v1.4.0**) — [Docs](https://masanori0209.github.io/hmscalc/) · [SemVer API guarantees](docs/API_STABILITY.md) · [Changelog](CHANGELOG.md) · [Roadmap](ROADMAP.md)

## Quick Start

```bash
pip install hmscalc
# or pin stable: pip install "hmscalc>=1.0,<2"
```

```python
from hmscalc import HMSTime

a = HMSTime("1:30:15")
b = HMSTime("2:15:45")

print(a + b)   # "3:46:00"
print(a - b)   # "-0:45:30"
print(a * 2)   # "3:00:30"
print(a / 2)   # "0:45:07"
```

## Why hmscalc?

| Approach | Limitation |
|----------|------------|
| `datetime.timedelta` | No `"1:30:15"` string parsing out of the box |
| Manual seconds math | Verbose; easy to mishandle negative values |
| `pytimeparse` | Parse-only — arithmetic is still on you |
| **hmscalc** | Parse **and** add / subtract / aggregate in one API |

## Features

- Addition, subtraction, and scalar multiply/divide
- Sum, average, min, and max of multiple values
- `HH:MM` and `HH:MM:SS` input (hours may exceed 24 — duration model)
- Negative durations, comparison operators, `datetime.timedelta` integration
- Input whitespace trimming (`" 1:30:15 "`)
- Type hints with `py.typed` marker
- Python **3.9** through **3.14**
- ISO 8601 duration (`from_iso8601` / `to_iso8601`) and custom `format()` (incl. zero-padded hours)
- `parse_many` / `sum_strings` for string iterables; mixed `timedelta` arithmetic
- Calendar helpers: month end, date ranges, gap detection (`hmscalc.dates`)
- Business-day calendar and holiday exclusion (`hmscalc.business_days`)
- Timezone helpers via stdlib `zoneinfo` (`hmscalc.tz`)
- Lenient parsing opt-in: `HMSTime("1:90:00", strict=False)` → `"2:30:00"`
- `HMSDateTime` — date + duration combined type
- Weekly/monthly bucket aggregation (`hmscalc.buckets`)
- Optional pandas extra: `pip install "hmscalc[pandas]"` → `hmscalc.pandas_extra`
- Meeting scheduling with buffers and business-day search (`hmscalc.scheduling`)
- CLI: `hmscalc add` / `sub` / `sum` / `avg` / `min` / `max` (+ `--format`, stdin)

## CLI

After `pip install hmscalc`:

```bash
hmscalc add 1:30 2:15 0:45
# 4:30:00

hmscalc sub 2:00 0:45
# 1:15:00

hmscalc sum 1:00 2:00 3:00
# 6:00:00

hmscalc avg 1:00 3:00
# 2:00:00

echo -e "1:00\n2:00" | hmscalc sum
# 3:00:00

hmscalc --format HH:MM add 1:30 2:00
# 3:30
```

Equivalent: `python -m hmscalc add 1:00 2:00`

## Usage

### Import

```python
from hmscalc import HMSTime
```

### Creating HMSTime (string vs seconds vs timedelta)

| Input | Recommended API | Example |
|-------|-----------------|---------|
| `"1:30:15"` string | `HMSTime("1:30:15")` | Human-readable durations |
| Integer seconds | `HMSTime.from_seconds(3661)` | Programmatic / computed values |
| `datetime.timedelta` | `HMSTime.from_timedelta(delta)` | Interop with stdlib datetime |

`HMSTime(...)` accepts **strings only**. Use `from_seconds()` for numeric seconds (`TypeError` if not `int`).

### Basic Operations

```python
a = HMSTime("1:30:15")
b = HMSTime("2:15:45")

print(a + b)            # "3:46:00"
print(a - b)            # "-0:45:30"
print(a > b)            # False
print(a.to_seconds())   # 5415
print(a.to_tuple())     # (1, 30, 15)
print(a.to_dict())      # {'hh': 1, 'mm': 30, 'ss': 15, 'negative': False}
```

### Scalar Operations

```python
HMSTime("1:00:00") * 3    # "3:00:00"
HMSTime("1:30:00") / 2    # "0:45:00"
2 * HMSTime("0:30:00")    # "1:00:00"
```

### Aggregation

```python
times = [HMSTime("1:30:15"), HMSTime("2:15:45"), HMSTime("0:45:30")]

HMSTime.sum(times)      # "4:31:30"
HMSTime.sum_strings(["1:30:15", "2:15:45", "0:45:30"])  # same
HMSTime.average(times)  # "1:30:30"
HMSTime.min(times)      # "0:45:30"
HMSTime.max(times)      # "2:15:45"
```

### timedelta Mixed Arithmetic

```python
import datetime

t = HMSTime("1:00:00")
print(t + datetime.timedelta(minutes=30))  # "1:30:00"
print(t - datetime.timedelta(minutes=15))  # "0:45:00"
```

### Work Time Example

```python
work_sessions = [
    HMSTime("2:15:30"),
    HMSTime("1:45:00"),
    HMSTime("0:30:15"),
]
print(HMSTime.sum(work_sessions))  # "4:30:45"
```

### timedelta Integration

```python
import datetime

t = HMSTime("1:30:15")
delta = t.to_timedelta()
restored = HMSTime.from_timedelta(delta)  # HMSTime("1:30:15")
```

### ISO 8601 Duration

```python
t = HMSTime.from_iso8601("PT1H30M15S")
print(t.to_iso8601())  # "PT1H30M15S"
print(str(t))          # "1:30:15"
```

Time section (`PT…`) and date parts (`P1D`, `P1W`, `P1DT2H`). Months/years use nominal lengths (30 / 365 days).

### Custom Output Format

```python
t = HMSTime("1:30:15")
t.format("HH:MM")            # "1:30"
t.format("HH:MM:SS")         # "1:30:15" — same as str(t)
t.format("HH:MM:SS:PADDED")  # "01:30:15" — zero-padded hours
```

### Calendar & Date Gaps (v1.1.0)

```python
from hmscalc import dates

dates.last_day_of_month(2026, 2)   # date(2026, 2, 28)
dates.days_in_month(2024, 2)         # 29

logged = [dates.parse_date("2026-06-01"), dates.parse_date("2026-06-03")]
dates.missing_dates(logged, dates.parse_date("2026-06-01"), dates.parse_date("2026-06-05"))
# [date(2026, 6, 2), date(2026, 6, 4), date(2026, 6, 5)]

dates.has_date_gaps(logged)  # True
dates.combine(dates.parse_date("2026-06-28"), "2:30:15")  # datetime
```

### Scheduling — find slots with buffers (v1.1.0)

1 時間の予定を入れたいとき、前後 15 分の余裕も含めて空きを探す例:

```python
from hmscalc import scheduling

busy = [
    ("2026-06-28 09:00", "2026-06-28 10:00"),
    ("2026-06-28 12:00", "2026-06-28 13:00"),
]

# 空き時間帯（開始可能な範囲）
windows = scheduling.find_availability_windows(
    busy,
    "2026-06-28 09:00",
    "2026-06-28 18:00",
    duration="1:00:00",
    buffer_before="0:15",
    buffer_after="0:15",
)
# 10:15〜10:45 開始可（12:00 前に終了+バッファが必要）
# 13:15〜16:45 開始可

# 15 分刻みの具体的な候補
slots = scheduling.find_availability_slots(
    busy,
    "2026-06-28 09:00",
    "2026-06-28 18:00",
    duration="1:00",
    buffer_before="0:15",
    buffer_after="0:15",
    step="0:15",
)
for slot in slots:
    print(slot.start, "→", slot.end)  # 予定本体
    print("  確保:", slot.reserved_start, "〜", slot.reserved_end)  # バッファ込み

# 複数日 × 稼働時間（9:00-18:00）
slots = scheduling.find_availability_across_days(
    busy,
    start_date=dates.parse_date("2026-06-28"),
    end_date=dates.parse_date("2026-06-30"),
    daily_start="9:00",
    daily_end="18:00",
    duration="1:00",
    buffer_before="0:15",
    buffer_after="0:15",
)
```

### Business Days & Timezones (v1.2.0)

```python
from datetime import date
from hmscalc import business_days, dates, scheduling, tz

# Mon–Fri with holidays
cal = business_days.BusinessCalendar.weekdays_only(
    holidays=[dates.parse_date("2026-01-01")],
)
business_days.add_business_days(date(2026, 6, 26), 1)  # Fri -> Mon

# Timezone-aware daily windows
start, end = tz.daily_window(date(2026, 6, 28), "9:00", "18:00", "Asia/Tokyo")
dt = tz.parse_datetime("2026-06-28 09:00", tz="Asia/Tokyo")

# Skip weekends and holidays when finding slots
slots = scheduling.find_availability_across_business_days(
    busy=[("2026-06-26 09:00", "2026-06-26 10:00")],
    start_date=date(2026, 6, 26),
    end_date=date(2026, 7, 3),
    calendar=cal,
    daily_start="9:00",
    daily_end="18:00",
    duration="1:00",
    tz="Asia/Tokyo",
)
```

### Lenient Mode, HMSDateTime & Buckets (v1.3.0)

```python
from datetime import date, timedelta
from hmscalc import HMSDateTime, HMSTime, buckets

# Opt-in overflow normalization
HMSTime("1:90:00", strict=False)  # "2:30:00"

# Date + duration combined type
point = HMSDateTime.from_strings("2026-06-28", "2:30")
point.to_datetime()
point + timedelta(hours=1)

# Weekly / monthly aggregation
records = [(date(2026, 6, 2), "1:00"), (date(2026, 6, 3), "2:30")]
for bucket in buckets.aggregate_by_week(records):
    print(bucket.period, bucket.total)

# pandas extra: pip install "hmscalc[pandas]"
# from hmscalc import pandas_extra
```

Documentation site: `poetry run mkdocs serve` — see [docs/index.md](docs/index.md).

### Error Handling

```python
from hmscalc import InvalidTimeFormatError, NotTimeStringError

HMSTime(" 1:30:15 ")   # OK — whitespace trimmed
HMSTime("1:99:00")     # InvalidTimeFormatError (use strict=False to normalize)
HMSTime(123)             # NotTimeStringError
```

### Negative Values

```python
t = HMSTime("-1:00:00")
print(str(t))           # "-1:00:00"
print(t.is_negative)    # True
print(t.to_seconds())   # -3600
print(t.to_dict())      # {'hh': 1, 'mm': 0, 'ss': 0, 'negative': True}
```

`to_tuple()` returns absolute `(hh, mm, ss)`; use `is_negative` or `to_seconds()` for sign.

### Hashable (sets and dict keys)

```python
a = HMSTime("1:00:00")
b = HMSTime("2:00:00")
sessions = {a, b, a}  # 2 unique items
```

## API Reference

### `HMSTime(time_str: str)`

Parse `HH:MM` or `HH:MM:SS`. Whitespace is trimmed. Hours may exceed 24 (duration model).

### Class methods

| Method | Description |
|--------|-------------|
| `HMSTime.from_seconds(total_seconds: int)` | Build from integer seconds |
| `HMSTime.from_timedelta(delta)` | Build from `datetime.timedelta` |
| `HMSTime.from_iso8601(duration)` | Build from ISO 8601 `PT…` duration |
| `HMSTime.sum(times)` | Sum iterable; empty → `"0:00:00"` |
| `HMSTime.sum_strings(strings)` | Parse and sum strings |
| `HMSTime.parse_many(strings)` | Parse strings to `list[HMSTime]` |
| `HMSTime.average(times)` | Mean, rounded to nearest second |
| `HMSTime.min(times)` / `HMSTime.max(times)` | Min / max of iterable |

### Instance methods & properties

| Member | Description |
|--------|-------------|
| `is_negative` | `True` if total seconds < 0 |
| `hh` / `mm` / `ss` | Absolute time components |
| `to_seconds()` | Integer total seconds (signed) |
| `to_minutes()` / `to_hours()` | Float conversion |
| `to_timedelta()` | `datetime.timedelta` |
| `to_iso8601()` | ISO 8601 `PT…` string |
| `format(fmt)` | `"HH:MM"`, `"HH:MM:SS"`, or `"HH:MM:SS:PADDED"` |
| `to_tuple()` | `(hh, mm, ss)` absolute components |
| `to_dict()` | `{'hh', 'mm', 'ss', 'negative'}` |

### Operators

`+`, `-`, `*`, `/` (scalar), `==`, `!=`, `<`, `<=`, `>`, `>=`

### Exceptions

```python
from hmscalc import HMSTimeError, InvalidTimeFormatError, NotTimeStringError, InvalidDateFormatError
```

| Exception | When |
|-------------|------|
| `InvalidTimeFormatError` | Bad format, mm/ss ≥ 60, empty string |
| `NotTimeStringError` | Non-string input |
| `HMSTimeError` | Base class for both |

## Input Rules

- Formats: `HH:MM` or `HH:MM:SS`
- Minutes and seconds: 0–59
- Optional leading `-` for negative durations
- Surrounding whitespace is ignored
- Strict by default; lenient opt-in via `strict=False` — see [Input Policy](docs/INPUT_POLICY.md)

## Development

See [CONTRIBUTING.md](CONTRIBUTING.md) for branching, CI, and release process.

```bash
poetry install
poetry run pytest --cov=hmscalc --cov-fail-under=95
```

Docker matrix (Python 3.9–3.14): `docker build -t hmscalc . && docker run --rm hmscalc ./runtests.sh`

## Links

- [PyPI](https://pypi.org/project/hmscalc/)
- [Changelog](CHANGELOG.md)
- [Contributing](CONTRIBUTING.md)
- [Security policy](SECURITY.md)
- [API stability policy](docs/API_STABILITY.md)
- [Migration guide](docs/MIGRATION.md)
- [Documentation](https://masanori0209.github.io/hmscalc/) — GitHub Pages (`poetry run mkdocs serve` locally)
- [Roadmap](ROADMAP.md)
- [Zenn: 作業時間を HH:MM で足し算する](https://zenn.dev/m2lab/articles/hmscalc-work-time-hhmm)
- [Zenn: PyPI 公開の記事](https://zenn.dev/m2lab/articles/454a3a0dd27dc8)

## License

[MIT License](LICENSE)
