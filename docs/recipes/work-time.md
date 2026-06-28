# 作業時間の集計

作業ログを `HH:MM` 文字列のまま足し合わせる例です。

```python
from hmscalc import HMSTime

sessions = ["2:15:30", "1:45:00", "0:30:15"]
print(HMSTime.sum_strings(sessions))  # "4:30:45"
print(HMSTime.average(HMSTime.parse_many(sessions)))
```

## timedelta との併用

```python
import datetime
from hmscalc import HMSTime

t = HMSTime("1:00:00")
print(t + datetime.timedelta(minutes=30))  # "1:30:00"
```

## 寛容モードで入力を正規化

スプレッドシート由来で `1:90` のような値がある場合:

```python
from hmscalc import HMSTime

normalized = HMSTime("1:90:00", strict=False)
print(normalized)  # "2:30:00"
```

## CLI

```bash
hmscalc sum 2:15:30 1:45:00 0:30:15
hmscalc avg 1:00 3:00
```
