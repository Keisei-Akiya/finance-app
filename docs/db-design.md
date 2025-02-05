# DB 設計

## ファイナンスアプリデータベース

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

| No. | カラム名       | 型          | 制約        | 備考          |
| --- | -------------- | ----------- | ----------- | ------------- |
| 1   | id             | SERIAL      | PRIMARY KEY | 銘柄 ID       |
| 2   | ticker         | VARCHAR(10) | NOT NULL    | 銘柄名        |
| 3   | name           | VARCHAR(50) | NOT NULL    | 名前          |
| 4   | start_date     | DATE        | NOT NULL    | 運用開始日    |
| 5   | asset_class_id | INTEGER     | FOREIGN KEY | 資産クラス ID |

## 価格履歴テーブル

円建ての調整済み終値

| No. | カラム名      | 型      | 制約        | 備考        |
| --- | ------------- | ------- | ----------- | ----------- |
| 1   | id            | SERIAL  | PRIMARY KEY | 価格履歴 ID |
| 2   | investment_id | INTEGER | FOREIGN KEY | 銘柄 ID     |
| 3   | date          | DATE    | NOT NULL    | 日付        |
| 4   | price         | DECIMAL | NOT NULL    | 価格        |

## 配当履歴テーブル

円建て

| No. | カラム名      | 型      | 制約        | 備考      |
| --- | ------------- | ------- | ----------- | --------- |
| 1   | id            | SERIAL  | PRIMARY KEY | 配当金 ID |
| 2   | investment_id | INTEGER | FOREIGN KEY | 銘柄 ID   |
| 3   | date          | DATE    | NOT NULL    | 日付      |
| 4   | amount        | DECIMAL | NOT NULL    | 金額      |

## 為替レートテーブル

1 相手通貨あたり何円か

| No. | カラム名    | 型      | 制約        | 備考      |
| --- | ----------- | ------- | ----------- | --------- |
| 1   | id          | SERIAL  | PRIMARY KEY | レート ID |
| 2   | currency_id | INTEGER | FOREIGN KEY | 通貨 ID   |
| 3   | date        | DATE    | NOT NULL    | 日付      |
| 4   | rate        | DECIMAL | NOT NULL    | レート    |

## リターンテーブル

| No. | カラム名      | 型      | 制約        | 備考        |
| --- | ------------- | ------- | ----------- | ----------- |
| 1   | id            | SERIAL  | PRIMARY KEY | リターン ID |
| 2   | investment_id | INTEGER | FOREIGN KEY | 銘柄 ID     |
| 3   | return        | DECIMAL | NOT NULL    | リターン    |

## 通貨テーブル

円の相手の通貨．

今後は他の通貨 シンガポール等 も追加するかもしれない．

| No. | カラム名 | 型         | 制約        | 備考    |
| --- | -------- | ---------- | ----------- | ------- |
| 1   | id       | SERIAL     | PRIMARY KEY | 通貨 ID |
| 2   | currency | VARCHAR(3) | NOT NULL    | 通貨    |

## 資産クラステーブル

Stock, Bond, REIT(不動産), Gold 等

| No. | カラム名 | 型          | 制約        | 備考          |
| --- | -------- | ----------- | ----------- | ------------- |
| 1   | id       | SERIAL      | PRIMARY KEY | 資産クラス ID |
| 2   | name     | VARCHAR(20) | NOT NULL    | 資産クラス名  |

## 参考文献

[厚生労働省「シームレスな健康情報活用基盤実証事業」地域連携システム テーブル定義書](!https://www.mhlw.go.jp/seisakunitsuite/bunya/kenkou_iryou/iryou/johoka/johokatsuyou/dl/tenpu03_06.pdf)
