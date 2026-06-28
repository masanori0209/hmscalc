# Input Policy

hmscalc defaults to **strict parsing** (v1.0 behavior). Lenient parsing is opt-in since v1.3.0.

## Strict mode (current and v1.0)

| Rule | Behavior |
|------|----------|
| Formats | `HH:MM`, `HH:MM:SS`, ISO 8601 time durations (`PT…`) |
| Minutes / seconds | Must be `0–59`; values like `1:90:00` raise `InvalidTimeFormatError` |
| Hours | Unbounded (duration model, not clock time) |
| Whitespace | Leading/trailing whitespace is trimmed |
| Sign | Optional leading `-` (HMS) or `-PT…` (ISO 8601) |
| Non-strings | `HMSTime(...)` requires `str`; use `from_seconds()` for integers |

## Lenient mode (opt-in since v1.3.0)

When ``strict=False`` is passed to ``HMSTime(...)``, ``HMSTime.parse(...)``, ``parse_many``, or ``sum_strings``:

| Rule | Behavior |
|------|----------|
| Overflow minutes/seconds | Normalized via total seconds (e.g. `"1:90:00"` → `"2:30:00"`) |
| Default | ``strict=True`` preserves v1.0 strict validation |

Use lenient mode only when you explicitly accept normalized input (e.g. spreadsheet exports).

## Rationale

- Strict validation catches data entry errors early.
- Normalization rules (carry minutes into hours, etc.) add ambiguity.
- v0.9.0 API freeze treats strict parsing as stable behavior for v1.0.

## Related

- README [Input Rules](../README.md#input-rules)
- ISO 8601: `from_iso8601` / `to_iso8601` — `PT…`, `P1D`, `P1W`, `P1DT2H` (nominal months/years)
