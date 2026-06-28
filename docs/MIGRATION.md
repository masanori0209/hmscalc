# Migration Guide

## Upgrading to v1.1.x from 1.0.x

v1.1.0 adds backward-compatible APIs only. Pin `hmscalc>=1.1,<2` to opt in.

### New in v1.1.0

| Area | API |
|------|-----|
| String iterables | `HMSTime.parse_many()`, `HMSTime.sum_strings()` |
| timedelta | `HMSTime ± datetime.timedelta` |
| Properties | `hh`, `mm`, `ss`, `abs()` |
| Format | `format("HH:MM:SS:PADDED")` |
| Dates | `from hmscalc import dates` — see README |
| CLI | `avg`, `min`, `max`, `--format`, stdin |
| Exceptions | `InvalidDateFormatError` |

## Upgrading to v1.0.x from 0.x

v1.0.0 is the first **stable** release (current: **1.0.7**). Patch releases 1.0.1–1.0.7 are dev/CI or docs updates only — no public API changes.

### Import path

Always import from the package root:

```python
from hmscalc import HMSTime, HMSTimeError, InvalidTimeFormatError, NotTimeStringError
```

This has been stable since v0.3.0.

### Notable API additions since 0.1.0

| Version | Change |
|---------|--------|
| 0.3.0 | Package root exports; exception types |
| 0.4.0 | Scalar `*` `/`, `__hash__`, `from_timedelta`, whitespace trim |
| 0.6.0 | CLI (`hmscalc add/sub/sum`), stricter `from_seconds()` |
| 0.7.0 | `from_iso8601` / `to_iso8601`, `format()` |
| 0.8.0 | Coverage and property tests (no API change) |

### `to_dict()` shape

Since v0.4.0, `to_dict()` includes a `negative` boolean key:

```python
{"hh": 1, "mm": 30, "ss": 15, "negative": False}
```

If you relied on pre-0.4.0 behavior without `negative`, update dict consumers accordingly.

### Input validation

Strict mode only: `mm` and `ss` must be 0–59. See [INPUT_POLICY.md](INPUT_POLICY.md).

### CLI

Available since v0.6.0:

```bash
pip install hmscalc
hmscalc sum 1:00 2:00
```

## v0.x → v1.0.0 checklist

1. Pin `hmscalc>=1.0.0,<2` in production.
2. Replace any private imports (`hmscalc.hms_time._…`) with public API.
3. Run your test suite; report issues via GitHub Security or Issues.

See [API_STABILITY.md](API_STABILITY.md) for long-term SemVer policy.
