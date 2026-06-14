---
title: "Python で作業時間を HH:MM 形式で足し算する"
emoji: "⏱️"
type: "tech"
topics: ["python", "pypi", "timedelta", "hmscalc"]
published: false
---

## はじめに

作業ログや学習時間を `"2:15:30"` のような文字列で持っているとき、`datetime.timedelta` だけではパースから演算まで一手間かかります。  
[hmscalc](https://pypi.org/project/hmscalc/) は **HH:MM / HH:MM:SS 文字列の加減算と集計** に特化した軽量ライブラリです。

```bash
pip install hmscalc
```

## ライブラリで集計する

```python
from hmscalc import HMSTime

sessions = [
    HMSTime("2:15:30"),
    HMSTime("1:45:00"),
    HMSTime("0:30:15"),
]

print(HMSTime.sum(sessions))  # 4:30:45
```

### 入力の使い分け

| データ | API |
|--------|-----|
| 文字列 `"1:30:00"` | `HMSTime("1:30:00")` |
| 秒数 `5400` | `HMSTime.from_seconds(5400)` |
| `timedelta` | `HMSTime.from_timedelta(delta)` |

## ターミナルから使う（CLI）

```bash
hmscalc add 1:30 2:15 0:45
# 4:30:00

hmscalc sub 5:00 1:30
# 3:30:00
```

シェルスクリプトや CI ログの集計にもそのまま使えます。

## timedelta との比較

| | hmscalc | timedelta |
|--|---------|-----------|
| `"1:30:15"` を直接パース | ✅ | ❌（別途変換） |
| 文字列での表示 | `"1:30:15"` | `1:30:15`（repr 依存） |
| 24時間超の duration | ✅ | ✅ |
| 標準ライブラリ | ❌ | ✅ |

hmscalc は **人間が読む時刻文字列** を扱う層、timedelta は **日時計算の基盤** として併用するのがおすすめです。

```python
delta = HMSTime("1:30:00").to_timedelta()
restored = HMSTime.from_timedelta(delta)
```

## まとめ

- 作業時間の足し算・引き算 → `HMSTime` + `sum` / 演算子
- コマンド一発 → `hmscalc add` / `sub` / `sum`
- PyPI: https://pypi.org/project/hmscalc/
- GitHub: https://github.com/masanori0209/hmscalc

---

> **Note:** このファイルは Zenn 公開用の下書きです。公開後は README のリンクを Zenn URL に差し替えてください。
