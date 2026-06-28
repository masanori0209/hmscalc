# hmscalc Roadmap

最終更新: 2026-06-28（v1.4.0 時点）

本ドキュメントは、hmscalc を「便利に使えるライブラリ」として広げるための打ち手を整理したものです。  
API の安定性ポリシーは [docs/API_STABILITY.md](docs/API_STABILITY.md) を参照してください。

## 現状（2026-06-28）

| 項目 | 状態 |
|------|------|
| バージョン | v1.4.0 |
| 公開 API | v1.0.0 から SemVer 保証 |
| 依存 | 標準ライブラリのみ（pandas は optional extra） |
| Python | 3.9〜3.14、CI 完備 |
| テスト | 190+ 件、カバレッジ ≥95% |
| ドキュメント | [GitHub Pages](https://masanori0209.github.io/hmscalc/) / Read the Docs |
| Zenn（公開済み） | [PyPI 公開の記事](https://zenn.dev/m2lab/articles/454a3a0dd27dc8)、[作業時間チュートリアル](https://zenn.dev/m2lab/articles/hmscalc-work-time-hhmm) |

---

## Phase 1 — 認知・採用

### 1.1 Zenn 記事（公開済み）

| 記事 | URL |
|------|-----|
| PyPI 公開の記録 | https://zenn.dev/m2lab/articles/454a3a0dd27dc8 |
| 作業時間チュートリアル | https://zenn.dev/m2lab/articles/hmscalc-work-time-hhmm |

### 1.2 PyPI / GitHub の見え方

- [x] README を Zenn URL・v1.1.0 に同期
- [x] GitHub Topics 追加（`python`, `duration`, `time-tracking`, `pypi` 等）
- [x] v1.2 計画用 meta Issue ([#65](https://github.com/masanori0209/hmscalc/issues/65))

---

## Phase 2 — v1.1.0（完了）

| 項目 | 状態 |
|------|------|
| `parse_many` / `sum_strings` | ✅ |
| `timedelta` 混在演算 | ✅ |
| CLI: `avg` / `min` / `max` / `--format` / stdin | ✅ |
| `hh` / `mm` / `ss` / `__abs__` | ✅ |
| `format("HH:MM:SS:PADDED")` | ✅ |
| 例外メッセージ改善（int → `from_seconds` ヒント） | ✅ |
| **日付ユーティリティ** (`hmscalc.dates`) | ✅ |
| **日程調整** (`hmscalc.scheduling`) — バッファ付き空き検索 | ✅ |

### 日付 API（v1.1.0）

```python
from hmscalc import dates

dates.last_day_of_month(2026, 2)          # date(2026, 2, 28)
dates.days_in_month(2024, 2)               # 29（うるう年）
dates.missing_dates(logged, start, end)   # 範囲内で記録のない日
dates.has_date_gaps(logged)                # 連続性に穴があるか
dates.gap_ranges(logged, start=..., end=...)  # 欠損区間 (first, last)
dates.combine(date(2026, 6, 28), "2:30")  # datetime 合成
dates.parse_date("2026-06-28")
dates.parse_datetime("2026-06-28 14:30:00")
dates.missing_datetimes(slots, start, end, step=timedelta(hours=1))
```

### 日程調整（scheduling）

```python
from hmscalc import scheduling

# 1時間の予定 + 前後15分バッファで空きを探す
slots = scheduling.find_availability_slots(
    busy=[("2026-06-28 09:00", "2026-06-28 10:00")],
    window_start="2026-06-28 09:00",
    window_end="2026-06-28 18:00",
    duration="1:00",
    buffer_before="0:15",
    buffer_after="0:15",
    step="0:15",
)
# slot.reserved_start / reserved_end でバッファ込みの占有範囲も確認可能
```

---

## Phase 3 — v1.2.0（完了）

| 項目 | 状態 |
|------|------|
| 営業日カレンダー（`hmscalc.business_days`） | ✅ |
| タイムゾーン helpers（`hmscalc.tz` / zoneinfo） | ✅ |
| 営業日のみ空き検索（`find_availability_across_business_days`） | ✅ |
| タイムゾーン付き日次検索（`find_availability_across_days(tz=...)`) | ✅ |
| Adversarial / Hypothesis テスト拡大 | ✅ |

### 営業日 API（v1.2.0）

```python
from datetime import date
from hmscalc import business_days, dates

cal = business_days.BusinessCalendar.weekdays_only(
    holidays=[dates.parse_date("2026-01-01")]
)
business_days.is_business_day(date(2026, 6, 29), calendar=cal)
business_days.add_business_days(date(2026, 6, 26), 1)  # Fri -> Mon
business_days.count_business_days(date(2026, 6, 1), date(2026, 6, 30))
```

### タイムゾーン API（v1.2.0）

```python
from hmscalc import tz

dt = tz.parse_datetime("2026-06-28 09:00", tz="Asia/Tokyo")
start, end = tz.daily_window(date(2026, 6, 28), "9:00", "18:00", "Asia/Tokyo")
utc = tz.local_to_utc(dt)
```

### 営業日 × スケジューリング

```python
from hmscalc import scheduling, business_days

slots = scheduling.find_availability_across_business_days(
    busy=[("2026-06-26 09:00", "2026-06-26 10:00")],
    start_date=date(2026, 6, 26),
    end_date=date(2026, 7, 3),
    calendar=business_days.BusinessCalendar.weekdays_only(holidays=[...]),
    daily_start="9:00",
    daily_end="18:00",
    duration="1:00",
    tz="Asia/Tokyo",  # optional
)
```

---

---

## Phase 3 — v1.3.0（完了）

| 項目 | 状態 |
|------|------|
| 寛容モード `strict=False` | ✅ |
| `HMSDateTime` 一体型 | ✅ |
| 週次・月次バケット集計（`hmscalc.buckets`） | ✅ |
| pandas extra（`hmscalc.pandas_extra`） | ✅ |
| MkDocs ドキュメントサイト | ✅ |

### 寛容モード

```python
HMSTime("1:90:00", strict=False)  # "2:30:00"
HMSTime.parse("0:90", strict=False)
```

### HMSDateTime

```python
from hmscalc import HMSDateTime

point = HMSDateTime.from_strings("2026-06-28", "2:30")
point.to_datetime()
point + timedelta(hours=1)
```

### バケット集計

```python
from hmscalc import buckets

buckets.aggregate_by_week([(date(2026, 6, 2), "1:00"), ...])
buckets.aggregate_by_month(records)
```

### pandas extra

```bash
pip install "hmscalc[pandas]"
```

```python
from hmscalc import pandas_extra
pandas_extra.aggregate_weekly(df, date_column="day", duration_column="duration")
```

### ドキュメントサイト

```bash
poetry install
poetry run mkdocs serve
poetry run mkdocs build
```

---

## Phase 3 — 残り（任意）

### 3.1 寛容モード（strict=False） — ✅ v1.3.0

### 3.2 日付・時刻の拡張（候補）

- [x] バッファ付き空き時間検索（`hmscalc.scheduling`）
- [x] 営業日カレンダー（祝日除外）— `hmscalc.business_days`
- [x] タイムゾーン helpers — `hmscalc.tz`
- [x] 週次・月次バケット集計 — `hmscalc.buckets`
- [x] `HMSDateTime` 型（日付 + HMSTime の一体型）
- [x] ISO 8601 日付部分（`P1D` / `P1W` / `P1DT…`、名目 M/Y）

### 3.3 エコシステム連携 — ✅ pandas extra

```toml
[tool.poetry.extras]
pandas = ["pandas"]
```

### 3.4 ドキュメントサイト — ✅ MkDocs

- [x] MkDocs + Material theme
- [x] `docs/recipes/` — 作業時間、日程調整、バケット集計
- [x] GitHub Pages デプロイ（`.github/workflows/docs.yml`）
- [x] Read the Docs 設定（`.readthedocs.yaml`）

---

## Phase 4 — メンテナンス

| 項目 | 内容 |
|------|------|
| Dependabot PR | 定期マージ |
| プロパティテスト | dates / CLI の Hypothesis 拡大 |
| ベンチマーク | timedelta 手書き vs hmscalc |

---

## 優先度サマリー

```
Phase 1（残り）
  └─ GitHub Topics
  └─ v1.2 meta Issue

Phase 3（完了）
  └─ v1.1–v1.4 機能（日付・scheduling・営業日・tz・buckets・pandas・docs）

Phase 4（継続）
  └─ CI / 依存 / テストの保守
```

---

## 関連リンク

- [API Stability Policy](docs/API_STABILITY.md)
- [Input Policy](docs/INPUT_POLICY.md)
- [Migration Guide](docs/MIGRATION.md)
- [Zenn 公開リポジトリ（m-zenn-dev）](https://github.com/masanori0209/m-zenn-dev)
