# API Stability Policy

hmscalc follows [Semantic Versioning 2.0](https://semver.org/) from **v1.0.0** onward.

## Public API (frozen at v1.0.0)

Symbols exported in `hmscalc.__all__`:

| Symbol | Kind |
|--------|------|
| `HMSTime` | Class |
| `HMSTimeError` | Exception |
| `InvalidTimeFormatError` | Exception |
| `NotTimeStringError` | Exception |

### `HMSTime` public surface

**Constructor:** `HMSTime(time_str: str)`

**Class methods:** `from_seconds`, `from_timedelta`, `from_iso8601`, `sum`, `average`, `min`, `max`

**Instance methods / properties:** `is_negative`, `format`, `to_seconds`, `to_minutes`, `to_hours`, `to_timedelta`, `to_iso8601`, `to_tuple`, `to_dict`

**Operators:** `+`, `-`, `*`, `/`, comparisons, `hash`

**CLI:** `hmscalc` console script (`add`, `sub`, `sum`)

Names prefixed with `_` are **not** public.

## SemVer commitments (v1.x)

| Change type | Version bump |
|-------------|--------------|
| Breaking API change | **Major** (2.0.0) |
| Backward-compatible feature | **Minor** (1.1.0) |
| Bug fix, docs, internal | **Patch** (1.0.1) |

## Deprecation policy

1. Mark deprecated APIs with `warnings.warn(..., DeprecationWarning)` for at least one **minor** release.
2. Document in CHANGELOG and MIGRATION.md.
3. Remove only in the next **major** release.

## v1.0.0 release checklist

- [x] Public API documented (README, package docstring)
- [x] Strict input policy decided ([INPUT_POLICY.md](INPUT_POLICY.md))
- [x] Test coverage ≥95%
- [x] Python 3.9–3.14 CI matrix
- [x] SECURITY.md and contribution guides
- [x] RC feedback period (v0.9.0)
- [x] Stable classifier on PyPI

## v1.4.0 additions (Minor)

- ISO 8601 date components: `P1D`, `P1W`, `P1DT2H`, nominal `P1M` / `P1Y`
- Documentation deployed via GitHub Pages and Read the Docs config

## v1.3.0 additions (Minor)

Backward-compatible features added in v1.3.0:

- `HMSTime(..., strict=False)` / `HMSTime.parse` — lenient overflow normalization
- `HMSDateTime` combined date + duration type
- `hmscalc.buckets` — weekly/monthly aggregation
- Optional `hmscalc[pandas]` extra and `hmscalc.pandas_extra`
- MkDocs documentation site

See [CHANGELOG.md](CHANGELOG.md) and [ROADMAP.md](ROADMAP.md).

## v1.2.0 additions (Minor)

Backward-compatible features added in v1.2.0:

- `hmscalc.business_days` module (weekday rules, holidays, add/count business days)
- `hmscalc.tz` module (zoneinfo-based parse, localize, daily windows)
- `scheduling.find_availability_across_business_days`, `find_availability_across_days(tz=...)`

See [CHANGELOG.md](CHANGELOG.md) and [ROADMAP.md](ROADMAP.md).

## v1.1.0 additions (Minor)

Backward-compatible features added in v1.1.0:

- `HMSTime.parse_many`, `sum_strings`, `± timedelta`, `hh`/`mm`/`ss`, `__abs__`, `format("HH:MM:SS:PADDED")`
- `hmscalc.dates` module and `InvalidDateFormatError`
- `hmscalc.scheduling` module (buffered availability search)
- CLI: `avg`, `min`, `max`, `--format`, stdin

See [CHANGELOG.md](CHANGELOG.md) and [ROADMAP.md](ROADMAP.md).

## Non-goals for v1.0

- Lenient overflow normalization (`1:90:00` → `2:30:00`)
- ISO 8601 date components (`P1D`)
- Optional dependencies beyond stdlib

These may be considered post-1.0 with explicit opt-in APIs.
