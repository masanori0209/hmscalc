# hmscalc

**HH:MM / HH:MM:SS** 形式の時間を Python で扱うためのライブラリです。

- 文字列のまま加減算・集計
- 日付・営業日・スケジューリング
- 週次・月次バケット集計
- 標準ライブラリのみ（pandas は optional extra）

```bash
pip install hmscalc
pip install "hmscalc[pandas]"  # pandas 連携
```

## クイックスタート

```python
from hmscalc import HMSTime

print(HMSTime("1:30") + HMSTime("2:15"))  # "3:45:00"
print(HMSTime.sum_strings(["1:00", "2:00", "3:00"]))  # "6:00:00"
```

## ドキュメント構成

| セクション | 内容 |
|-----------|------|
| [Getting Started](getting-started.md) | インストールと基本 API |
| [Recipes](recipes/work-time.md) | 実用例（作業時間、日程調整、集計） |
| [Reference](API_STABILITY.md) | API 安定性・入力ポリシー |

## リンク

- [GitHub](https://github.com/masanori0209/hmscalc)
- [PyPI](https://pypi.org/project/hmscalc/)
- [Changelog](../CHANGELOG.md)
