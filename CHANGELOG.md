# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

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

[0.7.0]: https://github.com/masanori0209/hmscalc/compare/v0.6.0...v0.7.0
[0.6.0]: https://github.com/masanori0209/hmscalc/compare/v0.5.0...v0.6.0
[0.5.0]: https://github.com/masanori0209/hmscalc/compare/v0.4.0...v0.5.0
[0.4.0]: https://github.com/masanori0209/hmscalc/compare/v0.3.1...v0.4.0
[0.3.1]: https://github.com/masanori0209/hmscalc/compare/v0.3.0...v0.3.1
[0.3.0]: https://github.com/masanori0209/hmscalc/compare/v0.2.0...v0.3.0
[0.2.0]: https://github.com/masanori0209/hmscalc/compare/v0.1.0...v0.2.0
[0.1.0]: https://github.com/masanori0209/hmscalc/releases/tag/v0.1.0
