# hmscalc

[![PyPI version](https://img.shields.io/pypi/v/hmscalc.svg)](https://pypi.org/project/hmscalc/)
[![Python versions](https://img.shields.io/pypi/pyversions/hmscalc.svg)](https://pypi.org/project/hmscalc/)
[![CI](https://github.com/masanori0209/hmscalc/actions/workflows/test.yml/badge.svg)](https://github.com/masanori0209/hmscalc/actions/workflows/test.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Add and subtract **HH:MM** / **HH:MM:SS** time strings in Python — no manual conversion to seconds required.

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

## Usage

### Import

```python
from hmscalc import HMSTime
```

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

### Error Handling

```python
from hmscalc import InvalidTimeFormatError, NotTimeStringError

HMSTime(" 1:30:15 ")   # OK — whitespace trimmed
HMSTime("1:99:00")     # InvalidTimeFormatError
HMSTime(123)             # NotTimeStringError
```

## Input Rules

- Formats: `HH:MM` or `HH:MM:SS`
- Minutes and seconds: 0–59
- Optional leading `-` for negative durations
- Surrounding whitespace is ignored

## Development

Requires Docker (optional) or Poetry locally.

```bash
# Local (Poetry)
poetry install
poetry run pytest

# Docker matrix (Python 3.9–3.14)
docker build -t hmscalc .
docker run --rm hmscalc ./runtests.sh
docker run --rm hmscalc ./lint.sh
```

## Links

- [PyPI](https://pypi.org/project/hmscalc/)
- [Changelog](CHANGELOG.md)
- [Zenn: PyPI 公開の記事](https://zenn.dev/m2lab/articles/454a3a0dd27dc8)

## License

[MIT License](LICENSE)
