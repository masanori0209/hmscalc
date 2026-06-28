# 週次・月次バケット集計

日付付きの作業時間レコードを週または月単位で合計します。

```python
from datetime import date
from hmscalc import buckets, HMSDateTime

records = [
    (date(2026, 6, 2), "1:00"),
    (date(2026, 6, 3), "2:30"),
    (date(2026, 6, 9), "0:45"),
    HMSDateTime.from_strings("2026-07-01", "1:15"),
]

weekly = buckets.aggregate_by_week(records)
for bucket in weekly:
    print(bucket.period, bucket.start, bucket.total, bucket.entry_count)

monthly = buckets.aggregate_by_month(records)
```

## pandas 連携

`pip install "hmscalc[pandas]"` 後:

```python
import pandas as pd
from hmscalc import pandas_extra

df = pd.DataFrame({
    "day": [date(2026, 6, 2), date(2026, 6, 3)],
    "duration": ["1:00", "2:30"],
})

weekly_df = pandas_extra.aggregate_weekly(df, date_column="day", duration_column="duration")
parsed = pandas_extra.parse_duration_series(df["duration"])
```

## 出力形式

`BucketTotal` の各フィールド:

| フィールド | 意味 |
|-----------|------|
| `period` | `"2026-W23"` または `"2026-06"` |
| `start` | 期間の開始日（週の月曜 / 月初） |
| `total` | 合計 `HMSTime` |
| `entry_count` | レコード件数 |
