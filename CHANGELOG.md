# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.4.0] - 2026-06-28

### Added

- ISO 8601 date components in `from_iso8601` / `to_iso8601`: `P1D`, `P1W`, `P1DT2H`, nominal `P1M` / `P1Y`
- GitHub Pages docs deploy workflow (`.github/workflows/docs.yml`)
- Read the Docs config (`.readthedocs.yaml`, `docs/requirements.txt`)

### Changed

- `to_iso8601()` emits `P1D` / `P1W` for whole-day/week durations instead of `PT24H` / `PT168H`
- PyPI `Documentation` URL points to GitHub Pages

## [1.3.0] - 2026-06-28

### Added

- Lenient parsing: `HMSTime(..., strict=False)`, `HMSTime.parse`, `parse_many`, `sum_strings` with `strict=False`
- `HMSDateTime` — combined calendar date and `HMSTime` with datetime arithmetic
- `hmscalc.buckets` — `aggregate_by_week`, `aggregate_by_month`, `BucketTotal`
- Optional pandas extra: `pip install hmscalc[pandas]` and `hmscalc.pandas_extra`
- MkDocs documentation site (`mkdocs.yml`, `docs/getting-started.md`, `docs/recipes/`)

## [1.2.0] - 2026-06-28

### Added

- `hmscalc.business_days` module: `BusinessCalendar`, `is_business_day`, `iter_business_days`, `business_day_range`, `count_business_days`, `add_business_days`, `next_business_day`, `previous_business_day`
- `hmscalc.tz` module: `parse_datetime`, `localize`, `to_timezone`, `local_to_utc`, `daily_window`, `time_on_date` (stdlib `zoneinfo`)
- `scheduling.find_availability_across_business_days` — skip weekends and holidays
- `scheduling.find_availability_across_days` — optional `tz` parameter for timezone-aware daily windows
- Adversarial and property tests for Phase 3 (business days, timezones, scheduling integration)

## [1.1.0] - 2026-06-28

### Added

- `HMSTime.parse_many()` / `HMSTime.sum_strings()` for string iterables
- `HMSTime` ± `datetime.timedelta` mixed arithmetic
- `hh` / `mm` / `ss` properties and `__abs__()`
- `format("HH:MM:SS:PADDED")` for zero-padded hours
- `hmscalc.dates` module: `parse_date`, `parse_datetime`, `monthrange`, `days_in_month`, `last_day_of_month`, `date_range`, `missing_dates`, `has_date_gaps`, `gap_ranges`, `combine`, `missing_datetimes`
- `hmscalc.scheduling` module: buffered availability search for meeting scheduling
- `InvalidDateFormatError` exception
- CLI: `avg`, `min`, `max`, `--format`, stdin input
- [ROADMAP.md](ROADMAP.md)

### Changed

- `NotTimeStringError` hints at `from_seconds()` when an `int` is passed
- README links to published Zenn tutorial

### Fixed

- `dates.gap_ranges`: empty `present` with explicit `start`/`end` now returns the full range as one gap

## [1.0.7] - 2026-06-15

### Changed

- README / CONTRIBUTING / MIGRATION synced with v1.0.6 state (coverage threshold, feature list)

## [1.0.6] - 2026-06-07

### Changed

- Dev dependency: pytest-cov 6.3.0 → 7.1.0
- CLI tests: in-process coverage for pytest-cov 7 compatibility

## [1.0.5] - 2026-06-07

### Changed

- CI: actions/setup-python 5.4.0 → 6.2.0

## [1.0.4] - 2026-06-07

### Changed

- CI: actions/checkout 4.2.2 → 6.0.3

## [1.0.3] - 2026-06-07

### Changed

- Dev dependency: isort 5.13.2 → 6.1.0

## [1.0.2] - 2026-06-07

### Changed

- Dev dependency: black 24.10.0 → 25.11.0

## [1.0.1] - 2026-06-07

### Changed

- Dev dependency: ruff 0.15.16 → 0.15.17

## [1.0.0] - 2026-06-07

### Added

- **Stable release** — public API SemVer guarantees ([API_STABILITY.md](docs/API_STABILITY.md))

### Changed

- PyPI classifier: `Development Status :: 5 - Production/Stable`
- README: stable badge and v1.0.0 notice

No breaking changes from v0.9.0.

## [0.9.0] - 2026-06-07

### Added

- API stability policy (`docs/API_STABILITY.md`) — public API freeze before v1.0
- Migration guide (`docs/MIGRATION.md`) for 0.x → 1.0 upgrades

### Note

This is the **release candidate** for v1.0.0. No breaking changes are planned before stable.

## [0.8.0] - 2026-06-07

### Added

- CI coverage threshold ≥95% (`--cov-fail-under=95`)
- Hypothesis property tests (Python 3.10+)
- `SECURITY.md`, Issue/PR templates, Dependabot config

### Changed

- GitHub Actions pinned to current stable (`checkout@v4.2.2`, `setup-python@v5.4.0`)

## [0.7.0] - 2026-06-07

### Added

- `HMSTime.from_iso8601()` / `to_iso8601()` for ISO 8601 time durations (`PT…`)
- `HMSTime.format()` with `HH:MM` and `HH:MM:SS`
- Input policy document (`docs/INPUT_POLICY.md`) — strict mode for v1.0

### Changed

- README: ISO 8601, format(), and input policy links

## [0.6.0] - 2026-06-07

### Added

- CLI: `hmscalc add`, `sub`, `sum` (and `python -m hmscalc`)
- `from_seconds()` raises `TypeError` for non-int input
- Zenn tutorial draft (`docs/articles/work-time-tutorial.md`)
- CLI subprocess tests

### Changed

- README: CLI section and input-path guidance (string vs seconds vs timedelta)

## [0.5.0] - 2026-06-07

### Added

- README API reference (class methods, operators, exceptions, negative values, hashable)
- Package module docstring documenting public API

### Changed

- CONTRIBUTING.md updated for current Poetry/CI/release workflow
- README links to CONTRIBUTING and v1.0.0 roadmap

## [0.4.0] - 2026-06-07

### Added

- Scalar multiply and divide (`HMSTime * 2`, `HMSTime / 2`, `2 * HMSTime`)
- `__hash__` support for use in sets and dict keys
- `py.typed` marker for PEP 561 type-checking support
- PyPI project URLs, keywords, and improved package description
- CI coverage reporting with pytest-cov
- README comparison table and pip-first quick start

### Changed

- Trim surrounding whitespace in time string input
- Refactor aggregation helpers with shared `_time_list` validation
- Unify Poetry installation in CI workflows (`pip install poetry`)
- Run tests before PyPI publish; update publish workflow actions

## [0.3.1] - 2026-06-07

### Changed

- Officially test and support Python 3.13 and 3.14 in CI and Docker matrix
- Add PyPI classifiers for Python 3.13 and 3.14

## [0.3.0] - 2026-06-07

### Added

- `HMSTime.average()`, `HMSTime.min()`, and `HMSTime.max()` class methods
- `HMSTime.from_timedelta()` and `HMSTime.to_timedelta()` for `datetime.timedelta` integration
- `HMSTime.is_negative` property
- `"negative"` key in `to_dict()` return value
- Package-level exports: `from hmscalc import HMSTime`
- Input validation: reject minute/second values >= 60
- Tests for edge cases, type errors, and new APIs (31 tests total)
- `poetry.lock` for reproducible dependency resolution
- `CHANGELOG.md`

### Fixed

- `to_dict()` now preserves sign information via the `"negative"` field
- Arithmetic (`+`, `-`) and comparison operators return `NotImplemented` for non-`HMSTime` operands
- `lint-check.sh` CLI commands (`black --check`, `isort --check-only`, `mypy`)
- Python 3.9 compatibility for type annotations (`from __future__ import annotations`)

### Changed

- Updated README with comparison operators, conversion methods, error handling, and input rules
- CI lint workflow now includes isort check
- Ruff updated from `^0.4.0` to `^0.15.0`

## [0.2.0] - 2025

### Added

- `HMSTime.sum()` class method for summing multiple time values

## [0.1.0] - Initial release

### Added

- `HMSTime` class with `HH:MM` / `HH:MM:SS` parsing
- Addition, subtraction, and comparison operators
- Conversion to seconds, minutes, hours, tuple, and dict
- Negative duration support
- Custom exceptions: `InvalidTimeFormatError`, `NotTimeStringError`

[1.1.0]: https://github.com/masanori0209/hmscalc/compare/v1.0.7...v1.1.0
[1.0.7]: https://github.com/masanori0209/hmscalc/compare/v1.0.6...v1.0.7
[1.0.6]: https://github.com/masanori0209/hmscalc/compare/v1.0.5...v1.0.6
[1.0.5]: https://github.com/masanori0209/hmscalc/compare/v1.0.4...v1.0.5
[1.0.4]: https://github.com/masanori0209/hmscalc/compare/v1.0.3...v1.0.4
[1.0.3]: https://github.com/masanori0209/hmscalc/compare/v1.0.2...v1.0.3
[1.0.2]: https://github.com/masanori0209/hmscalc/compare/v1.0.1...v1.0.2
[1.0.1]: https://github.com/masanori0209/hmscalc/compare/v1.0.0...v1.0.1
[1.0.0]: https://github.com/masanori0209/hmscalc/compare/v0.9.0...v1.0.0
[0.9.0]: https://github.com/masanori0209/hmscalc/compare/v0.8.0...v0.9.0
[0.8.0]: https://github.com/masanori0209/hmscalc/compare/v0.7.0...v0.8.0
[0.7.0]: https://github.com/masanori0209/hmscalc/compare/v0.6.0...v0.7.0
[0.6.0]: https://github.com/masanori0209/hmscalc/compare/v0.5.0...v0.6.0
[0.5.0]: https://github.com/masanori0209/hmscalc/compare/v0.4.0...v0.5.0
[0.4.0]: https://github.com/masanori0209/hmscalc/compare/v0.3.1...v0.4.0
[0.3.1]: https://github.com/masanori0209/hmscalc/compare/v0.3.0...v0.3.1
[0.3.0]: https://github.com/masanori0209/hmscalc/compare/v0.2.0...v0.3.0
[0.2.0]: https://github.com/masanori0209/hmscalc/compare/v0.1.0...v0.2.0
[0.1.0]: https://github.com/masanori0209/hmscalc/releases/tag/v0.1.0
