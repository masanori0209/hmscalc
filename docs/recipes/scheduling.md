# 日程調整 — バッファ付き空き検索

```python
from datetime import date
from hmscalc import business_days, scheduling

busy = [("2026-06-28 09:00", "2026-06-28 10:00")]

slots = scheduling.find_availability_slots(
    busy,
    "2026-06-28 09:00",
    "2026-06-28 18:00",
    duration="1:00",
    buffer_before="0:15",
    buffer_after="0:15",
    step="0:15",
)

for slot in slots:
    print(slot.start, "→", slot.end)
    print("  確保:", slot.reserved_start, "〜", slot.reserved_end)
```

## 営業日のみ

```python
cal = business_days.BusinessCalendar.weekdays_only(holidays=[])

slots = scheduling.find_availability_across_business_days(
    busy,
    start_date=date(2026, 6, 26),
    end_date=date(2026, 7, 3),
    calendar=cal,
    daily_start="9:00",
    daily_end="18:00",
    duration="1:00",
    tz="Asia/Tokyo",
)
```

## タイムゾーン

```python
from hmscalc import tz

start, end = tz.daily_window(date(2026, 6, 28), "9:00", "18:00", "Asia/Tokyo")
```
