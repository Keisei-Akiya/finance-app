# DB 設計

## テーブル一覧

| No. | テーブル名      | 種別             | 備考           |
| --- | --------------- | ---------------- | -------------- |
| 1   | investment_info | マスタ           | 銘柄情報       |
| 2   | price           | トランザクション | 価格履歴       |
| 3   | dividend        | トランザクション | 配当履歴       |
| 4   | exchange_rate   | トランザクション | 為替レート履歴 |
| 5   | return          | トランザクション | リターン       |
| 6   | currency        | マスタ           | 通貨           |
| 7   | asset_class     | マスタ           | 資産クラス     |

## 投資銘柄情報テーブル

| No. | カラム名        | 型          | 制約        | 備考                      |
| --- | --------------- | ----------- | ----------- | ------------------------- |
| 1   | investment_id   | serial      | PRIMARY KEY | 銘柄 ID                   |
| 2   | ticker          | varchar(7)  | NOT NULL    | `yfinance` 用のティッカー |
| 3   | investment_name | varchar(50) | NOT NULL    | 名前                      |
| 4   | start_date      | date        | NOT NULL    | 運用開始日                |
| 5   | asset_class_id  | serial      | FOREIGN KEY | 資産クラス ID             |

## 価格履歴テーブル

円建ての調整済み終値

| No. | カラム名      | 型            | 制約        | 備考                                          |
| --- | ------------- | ------------- | ----------- | --------------------------------------------- |
| 1   | price_id      | serial        | PRIMARY KEY | 価格履歴 ID                                   |
| 2   | investment_id | serial        | FOREIGN KEY | 銘柄 ID                                       |
| 3   | date          | date          | NOT NULL    | 日付                                          |
| 4   | price         | numeric[8, 2] | NOT NULL    | 価格<br>制度 8<br>スケール 2<br>最大 99999.99 |

## 配当履歴テーブル

円建て

| No. | カラム名      | 型            | 制約        | 備考                                                        |
| --- | ------------- | ------------- | ----------- | ----------------------------------------------------------- |
| 1   | dividend_id   | serial        | PRIMARY KEY | 配当金 ID                                                   |
| 2   | investment_id | serial        | FOREIGN KEY | 銘柄 ID                                                     |
| 3   | date          | date          | NOT NULL    | 日付                                                        |
| 4   | dividend      | numeric[8, 2] | NOT NULL    | 1 株当たり配当金額<br>制度 8<br>スケール 2<br>最大 99999.99 |

## 為替レートテーブル

1 相手通貨あたり何円か

| No. | カラム名         | 型            | 制約        | 備考                                                                          |
| --- | ---------------- | ------------- | ----------- | ----------------------------------------------------------------------------- |
| 1   | exchange_rate_id | serial        | PRIMARY KEY | 為替レート ID                                                                 |
| 2   | currency_id      | serial        | FOREIGN KEY | 通貨 ID                                                                       |
| 3   | date             | date          | NOT NULL    | 日付                                                                          |
| 4   | exchange_rate    | numeric[8, 2] | NOT NULL    | 為替レート<br>1 相手通貨当たり日本円<br>制度 8<br>スケール 2<br>最大 99999.99 |

## リターンテーブル

| No. | カラム名      | 型            | 制約        | 備考                                                                    |
| --- | ------------- | ------------- | ----------- | ----------------------------------------------------------------------- |
| 1   | return_id     | serial        | PRIMARY KEY | リターン ID                                                             |
| 2   | investment_id | serial        | FOREIGN KEY | 銘柄 ID                                                                 |
| 3   | return        | numeric[8, 2] | NOT NULL    | CAGR (年率平均成長率)<br>%表記<br>制度 8<br>スケール 2<br>最大 99999.99 |

## 通貨テーブル

円の相手の通貨．

今後は他の通貨 シンガポールドル等 も追加するかもしれない．

| No. | カラム名      | 型          | 制約        | 備考                                           |
| --- | ------------- | ----------- | ----------- | ---------------------------------------------- |
| 1   | currency_id   | varchar(3)  | PRIMARY KEY | 通貨コード (ISO 4217)<br>USD 等の一意の 3 文字 |
| 2   | currency_name | varchar(50) | NOT NULL    | 通貨名<br>例: アメリカドル                     |

## 資産クラステーブル

Stock, Bond, REIT(不動産), Gold 等

| No. | カラム名         | 型          | 制約        | 備考                                           |
| --- | ---------------- | ----------- | ----------- | ---------------------------------------------- |
| 1   | asset_class_id   | serial      | PRIMARY KEY | 資産クラス ID                                  |
| 2   | asset_class_name | varchar(10) | NOT NULL    | 資産クラス名<br>例: 株式，債券，REIT，ゴールド |

## 参考文献

[厚生労働省「シームレスな健康情報活用基盤実証事業」地域連携システム テーブル定義書](!https://www.mhlw.go.jp/seisakunitsuite/bunya/kenkou_iryou/iryou/johoka/johokatsuyou/dl/tenpu03_06.pdf)

[PostgreSQL 9.4.5 文書 第 8 章 データ型](!https://www.postgresql.jp/docs/9.4/datatype.html)

[国別通貨コード一覧 (ISO 4217)](!https://www.iban.jp/currency-codes)
