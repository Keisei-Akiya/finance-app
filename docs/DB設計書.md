# DB 設計

- 銘柄情報テーブル
- 価格履歴テーブル
- 平均分散テーブル

## 銘柄情報テーブル

```plant
銘柄情報テーブル (StockInfo)
  * 銘柄 ID (StockID)
  --
  * 銘柄名 (Ticker)
  * 名前 (Name)
```

## 価格履歴テーブル

```plant
価格履歴テーブル (PriceHistory)
  * 価格履歴 ID (PriceHistoryID)
  --
  * 銘柄 ID (StockID)
  * 日付 (Date)
  * 価格 (Price)
```

## 平均分散テーブル

```plant
平均分散テーブル (MeanVariance)
  * 平均分散 ID (MeanVarianceID)
  --
  * 銘柄 ID (StockID)
  * 平均 (Mean)
  * 分散 (Variance)
```
