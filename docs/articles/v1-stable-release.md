---
title: "hmscalc v1.0.0 — Stable リリース"
emoji: "🎉"
type: "tech"
topics: ["python", "pypi", "hmscalc", "release"]
published: false
---

## hmscalc v1.0.0 が Stable になりました

[hmscalc](https://pypi.org/project/hmscalc/) は HH:MM / HH:MM:SS 形式の時刻演算ライブラリです。
v1.0.0 から **SemVer に基づく API 安定性** を保証します。

```bash
pip install "hmscalc>=1.0.0,<2"
```

## v1.0.0 で確定した API

- `HMSTime` — 加減算、スカラー演算、集計
- `from_seconds` / `from_timedelta` / `from_iso8601`
- CLI: `hmscalc add` / `sub` / `sum`
- 例外: `HMSTimeError`, `InvalidTimeFormatError`, `NotTimeStringError`

詳細: [API Stability Policy](https://github.com/masanori0209/hmscalc/blob/main/docs/API_STABILITY.md)

## 0.x からのアップグレード

破壊的変更は v0.9.0 → v1.0.0 間ではありません。
[Migration Guide](https://github.com/masanori0209/hmscalc/blob/main/docs/MIGRATION.md) を参照してください。

## 今後

- **Minor** (1.1.0): 後方互換の機能追加
- **Patch** (1.0.x): バグ修正
- **Major** (2.0.0): 破壊的変更（事前 deprecation あり）

---

> **Note:** Zenn 公開用下書き。公開後 README のリンクを更新してください。
