# Input Policy

hmscalc v1.0 uses **strict parsing only**. This document records the decision for issue #29.

## Strict mode (current and v1.0)

| Rule | Behavior |
|------|----------|
| Formats | `HH:MM`, `HH:MM:SS`, ISO 8601 time durations (`PT…`) |
| Minutes / seconds | Must be `0–59`; values like `1:90:00` raise `InvalidTimeFormatError` |
| Hours | Unbounded (duration model, not clock time) |
| Whitespace | Leading/trailing whitespace is trimmed |
| Sign | Optional leading `-` (HMS) or `-PT…` (ISO 8601) |
| Non-strings | `HMSTime(...)` requires `str`; use `from_seconds()` for integers |

## Lenient mode (not planned for v1.0)

Normalizing overflow (e.g. `"1:90:00"` → `"2:30:00"`) is **out of scope** for v1.0.
If added later, it would be opt-in (e.g. a parameter or separate parser) to avoid breaking strict callers.

## Rationale

- Strict validation catches data entry errors early.
- Normalization rules (carry minutes into hours, etc.) add ambiguity.
- v0.9.0 API freeze treats strict parsing as stable behavior for v1.0.

## Related

- README [Input Rules](../README.md#input-rules)
- ISO 8601: `HMSTime.from_iso8601()` / `to_iso8601()` (time section only; no `P1D` date part)
