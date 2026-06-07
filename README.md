# hmscalc

[![PyPI version](https://img.shields.io/pypi/v/hmscalc.svg)](https://pypi.org/project/hmscalc/)
[![Python versions](https://img.shields.io/pypi/pyversions/hmscalc.svg)](https://pypi.org/project/hmscalc/)

A lightweight Python library for performing arithmetic on time values formatted as `HH:MM` or `HH:MM:SS`.

## 🚀 Features

- Supports time addition and subtraction
- Sum, average, min, and max of multiple time values
- Accepts `HH:MM` and `HH:MM:SS` formatted strings
- Handles negative durations gracefully
- Comparison operators (`==`, `!=`, `<`, `<=`, `>`, `>=`)
- Converts time to seconds, minutes, hours, timedelta, and dictionary/tuple formats
- Integration with `datetime.timedelta`
- Custom exceptions for invalid input
- Fully testable across multiple Python versions via Docker

## 🐳 Quick Start (Docker-based)

```bash
# Build the image
docker build -t hmscalc .

# Run tests across multiple Python versions
docker run --rm hmscalc ./runtests.sh

# Run lint
docker run --rm hmscalc ./lint.sh
```

## 📦 Project Structure

```
hmscalc/
├── Dockerfile         # Docker setup with pyenv and poetry
├── runtests.sh        # Runs tests on multiple Python versions
├── hmscalc/           # Source code
│   ├── hms_time.py
│   └── exceptions.py
├── tests/             # Pytest-based unit tests
├── pyproject.toml     # Poetry config
├── README.md          # This file
└── LICENSE            # MIT license
```

## 📚 Usage (inside container)

### Import

```python
from hmscalc import HMSTime
# or
from hmscalc.hms_time import HMSTime
```

### Basic Operations

```python
a = HMSTime("1:30:15")
b = HMSTime("2:15:45")

print(a + b)            # "3:46:00"
print(a - b)            # "-0:45:30"
print(a > b)            # False
print(a.to_seconds())   # 5415
print(a.to_minutes())   # 90.25
print(a.to_hours())     # 1.504...
print(a.to_tuple())     # (1, 30, 15)
print(a.to_dict())      # {'hh': 1, 'mm': 30, 'ss': 15, 'negative': False}
```

### Negative Values

```python
t = HMSTime("-1:00:00")
print(t.to_seconds())   # -3600
print(t.is_negative)    # True
print(t.to_dict())      # {'hh': 1, 'mm': 0, 'ss': 0, 'negative': True}
```

### Sum / Average / Min / Max

```python
times = [
    HMSTime("1:30:15"),
    HMSTime("2:15:45"),
    HMSTime("0:45:30"),
]

print(HMSTime.sum(times))      # "4:31:30"
print(HMSTime.average(times))  # "1:30:30"
print(HMSTime.min(times))      # "0:45:30"
print(HMSTime.max(times))      # "2:15:45"
print(HMSTime.sum([]))         # "0:00:00"
```

### timedelta Integration

```python
import datetime

t = HMSTime("1:30:15")
delta = t.to_timedelta()                          # datetime.timedelta(...)
restored = HMSTime.from_timedelta(delta)          # HMSTime("1:30:15")
```

### Error Handling

```python
from hmscalc import InvalidTimeFormatError, NotTimeStringError

try:
    HMSTime("1:99:00")   # minute >= 60
except InvalidTimeFormatError:
    pass

try:
    HMSTime(123)         # non-string input
except NotTimeStringError:
    pass
```

## 📋 Input Rules

- Formats: `HH:MM` or `HH:MM:SS` (hours may exceed 24 — duration model)
- Minutes and seconds must be in the range 0–59
- Optional leading `-` for negative durations
- Input must be a string

## 🔍 Examples

### Basic Arithmetic
```python
HMSTime("2:30") + HMSTime("1:45")     # "4:15:00"
HMSTime("1:00:30") - HMSTime("0:30")  # "0:30:30"
HMSTime("0:00") - HMSTime("0:01")     # "-0:01:00"
```

### Work Time Calculation
```python
work_sessions = [
    HMSTime("2:15:30"),
    HMSTime("1:45:00"),
    HMSTime("0:30:15"),
]
total_work = HMSTime.sum(work_sessions)
print(f"Total work time: {total_work}")  # "4:30:45"
```

## 🧪 Running tests locally via Docker

```bash
# Build image
docker build -t hmscalc .

# Run matrix tests via pyenv + poetry
docker run --rm hmscalc ./runtests.sh
```

## 📄 License

This project is licensed under the [MIT License](LICENSE).
