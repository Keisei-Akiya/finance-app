# DB 設計

- 投資銘柄情報テーブル
- 価格履歴テーブル
- 配当履歴テーブル
- 為替レートテーブル
- リターンテーブル
- 通貨テーブル
- 資産クラステーブル

## 投資銘柄情報テーブル

```plant
投資銘柄情報テーブル (InvestmentInfo)
  * 銘柄 ID (InvestmentInfoID)
  --
  * 銘柄名 (Ticker):
  * 名前 (Name)
  * 運用開始日 (StartDate): date
  * 資産クラス ID (AssetClassID 外部キー)
```

## 価格履歴テーブル

円建ての調整済み終値

```plant
価格履歴テーブル (PriceHistory)
  * 価格履歴 ID (PriceHistoryID)
  --
  * 銘柄 ID (InvestmentID 外部キー)
  * 日付 (Date): date
  * 価格 (Price)
```

## 配当履歴テーブル

円建て

```plant
配当履歴テーブル (Dividend)
  * 配当金 ID (DividendID)
  --
  * 銘柄 ID (InvestmentID 外部キー)
  * 日付 (Date): date
  * 金額 (Amount)
```

## 為替レートテーブル

1 相手通貨あたり何円か

```plant
為替レートテーブル (ExchangeRate)
  * レート ID (RateID)
  --
  * 通貨ID (CurrencyID 外部キー)
  * 日付 (Date): date
  * レート (Rate)
```

## リターンテーブル

```plant
リターンテーブル (Return)
  * リターン ID (ReturnID)
  --
  * 銘柄 ID (InvestmentID 外部キー)
  * リターン (Return)
```

## 通貨テーブル

円の相手の通貨．

今後は他の通貨 シンガポール等 も追加するかもしれない．

```plant
通貨テーブル (Currency)
  * 通貨ペア ID (CurrencyID)
  --
  * ドル (USD)
```

## 資産クラステーブル

Stock, Bond, REIT(不動産), Gold 等

```plant
資産クラステーブル (AssetClass)
  * 資産クラス ID (AssetClassID)
  --
  * 資産クラス名 (AssetClassName)
```
