# DB 設計

- 銘柄情報テーブル
- 価格履歴テーブル
- 配当テーブル
- ドル円レートテーブル

## 投資情報テーブル

```plant
投資情報テーブル (InvestmentInfo)
  * 銘柄 ID (InvestmentInfoID)
  --
  * 銘柄名 (Ticker)
  * 名前 (Name)
  * 運用開始日 (StartDate)
  * 資産クラス ID (AssetClassID 外部キー)
```

## 価格履歴テーブル

円建ての調整済み終値

```plant
価格履歴テーブル (PriceHistory)
  * 価格履歴 ID (PriceHistoryID)
  --
  * 銘柄 ID (InvestmentID 外部キー)
  * 日付 (Date)
  * 価格 (Price)
```

## 配当履歴テーブル

円建て

```plant
配当履歴テーブル (Dividend)
  * 配当金 ID (DividendID)
  --
  * 銘柄 ID (InvestmentID 外部キー)
  * 日付 (Date)
  * 金額 (Amount)
```

## 為替レートテーブル

```plant
為替レートテーブル (ExchangeRate)
  * レート ID (RateID)
  --
  * 通貨ID (CurrencyID 外部キー)
  * 日付 (Date)
  * レート (Rate)
```

## 通貨テーブル

円の相手の通貨．

今後は他の通貨も追加するかもしれない．

```plant
通貨ペアテーブル (Currency)
  * 通貨ペア ID (CurrencyID)
  --
  * ドル (USD)
```

## 資産クラステーブル

```plant
資産クラステーブル (AssetClass)
  * 資産クラス ID (AssetClassID)
  --
  * 株式 (Stock)
  * 債券 (Bond)
  * REIT (REIT)
  * 金 (Gold)
```
