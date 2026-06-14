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
- [ ] RC feedback period (v0.9.0)
- [ ] Stable classifier on PyPI

## Non-goals for v1.0

- Lenient overflow normalization (`1:90:00` → `2:30:00`)
- ISO 8601 date components (`P1D`)
- Optional dependencies beyond stdlib

These may be considered post-1.0 with explicit opt-in APIs.
