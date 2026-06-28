# Getting Started

## インストール

```bash
pip install hmscalc
```

SemVer 安定版を pin する場合:

```bash
pip install "hmscalc>=1.0,<2"
```

pandas 連携:

```bash
pip install "hmscalc[pandas]"
```

## HMSTime — 基本

```python
from hmscalc import HMSTime

a = HMSTime("1:30:15")
b = HMSTime("2:15:45")

print(a + b)           # "3:46:00"
print(a.to_seconds())  # 5415
print(a.to_timedelta())
```

### 寛容モード（`strict=False`）

オーバーフローする分・秒を正規化します（デフォルトは strict）。

```python
strict = HMSTime("1:90:00")          # InvalidTimeFormatError
lenient = HMSTime("1:90:00", strict=False)  # "2:30:00"
same = HMSTime.parse("1:90:00", strict=False)
```

## HMSDateTime — 日付 + 時間

```python
from hmscalc import HMSDateTime

point = HMSDateTime.from_strings("2026-06-28", "2:30:15")
print(point.to_datetime())
print(point + __import__("datetime").timedelta(hours=1))
```

## 日付・営業日・タイムゾーン

```python
from datetime import date
from hmscalc import business_days, dates, tz

dates.last_day_of_month(2026, 2)
business_days.add_business_days(date(2026, 6, 26), 1)
tz.parse_datetime("2026-06-28 09:00", tz="Asia/Tokyo")
```

## 週次・月次集計

```python
from datetime import date
from hmscalc import buckets

records = [
    (date(2026, 6, 2), "1:00"),
    (date(2026, 6, 3), "2:30"),
    (date(2026, 7, 1), "0:45"),
]

for bucket in buckets.aggregate_by_week(records):
    print(bucket.period, bucket.total, bucket.entry_count)
```

## CLI

```bash
hmscalc add 1:30 2:15
hmscalc sum 1:00 2:00 3:00
hmscalc avg 1:00 3:00
```

## 次のステップ

- [作業時間のレシピ](recipes/work-time.md)
- [日程調整](recipes/scheduling.md)
- [バケット集計](recipes/buckets.md)
- [Input Policy](INPUT_POLICY.md)
