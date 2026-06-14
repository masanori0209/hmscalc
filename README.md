# hmscalc

[![PyPI version](https://img.shields.io/pypi/v/hmscalc.svg)](https://pypi.org/project/hmscalc/)
[![Stable](https://img.shields.io/badge/status-stable-green.svg)](docs/API_STABILITY.md)
[![Python versions](https://img.shields.io/pypi/pyversions/hmscalc.svg)](https://pypi.org/project/hmscalc/)
[![CI](https://github.com/masanori0209/hmscalc/actions/workflows/test.yml/badge.svg)](https://github.com/masanori0209/hmscalc/actions/workflows/test.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Add and subtract **HH:MM** / **HH:MM:SS** time strings in Python — no manual conversion to seconds required.

**v1.0.0** is the first stable release with [SemVer API guarantees](docs/API_STABILITY.md).

## Quick Start

```bash
pip install hmscalc
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
- CLI: `hmscalc add` / `sub` / `sum` from the terminal

## CLI

After `pip install hmscalc`:

```bash
hmscalc add 1:30 2:15 0:45
# 4:30:00

hmscalc sub 2:00 0:45
# 1:15:00

hmscalc sum 1:00 2:00 3:00
# 6:00:00
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
HMSTime.average(times)  # "1:30:30"
HMSTime.min(times)      # "0:45:30"
HMSTime.max(times)      # "2:15:45"
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

Time section only (`PT…`); date parts like `P1D` are not supported.

### Custom Output Format

```python
t = HMSTime("1:30:15")
t.format("HH:MM")     # "1:30"
t.format("HH:MM:SS")  # "1:30:15" — same as str(t)
```

### Error Handling

```python
from hmscalc import InvalidTimeFormatError, NotTimeStringError

HMSTime(" 1:30:15 ")   # OK — whitespace trimmed
HMSTime("1:99:00")     # InvalidTimeFormatError
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
| `HMSTime.average(times)` | Mean, rounded to nearest second |
| `HMSTime.min(times)` / `HMSTime.max(times)` | Min / max of iterable |

### Instance methods & properties

| Member | Description |
|--------|-------------|
| `is_negative` | `True` if total seconds < 0 |
| `to_seconds()` | Integer total seconds (signed) |
| `to_minutes()` / `to_hours()` | Float conversion |
| `to_timedelta()` | `datetime.timedelta` |
| `to_iso8601()` | ISO 8601 `PT…` string |
| `format(fmt)` | `"HH:MM"` or `"HH:MM:SS"` (`__str__` = `format("HH:MM:SS")`) |
| `to_tuple()` | `(hh, mm, ss)` absolute components |
| `to_dict()` | `{'hh', 'mm', 'ss', 'negative'}` |

### Operators

`+`, `-`, `*`, `/` (scalar), `==`, `!=`, `<`, `<=`, `>`, `>=`

### Exceptions

```python
from hmscalc import HMSTimeError, InvalidTimeFormatError, NotTimeStringError
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
- Strict mode only: overflow minutes/seconds (e.g. `1:90:00`) are rejected — see [Input Policy](docs/INPUT_POLICY.md)

## Development

See [CONTRIBUTING.md](CONTRIBUTING.md) for branching, CI, and release process.

```bash
poetry install
poetry run pytest --cov=hmscalc
```

Docker matrix (Python 3.9–3.14): `docker build -t hmscalc . && docker run --rm hmscalc ./runtests.sh`

## Links

- [PyPI](https://pypi.org/project/hmscalc/)
- [Changelog](CHANGELOG.md)
- [Contributing](CONTRIBUTING.md)
- [Security policy](SECURITY.md)
- [API stability policy](docs/API_STABILITY.md)
- [Migration guide](docs/MIGRATION.md)
- [Roadmap (v1.0.0)](https://github.com/masanori0209/hmscalc/issues/20)
- [Zenn: v1.0.0 Stable リリース（下書き）](docs/articles/v1-stable-release.md)
- [Zenn: 作業時間を HH:MM で足し算する（チュートリアル）](docs/articles/work-time-tutorial.md) — 公開用下書き
- [Zenn: PyPI 公開の記事](https://zenn.dev/m2lab/articles/454a3a0dd27dc8)

## License

[MIT License](LICENSE)
