# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

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

[0.3.0]: https://github.com/masanori0209/hmscalc/compare/v0.2.0...v0.3.0
[0.2.0]: https://github.com/masanori0209/hmscalc/compare/v0.1.0...v0.2.0
[0.1.0]: https://github.com/masanori0209/hmscalc/releases/tag/v0.1.0
