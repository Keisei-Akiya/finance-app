# 機能設計書

## 機能一覧

- Lambda 1 ダウンロード & 日本円建てを 67 DB 登録
- Lambda 2 リターンを計算して DB に登録
- Lambda 3 ポートフォリオの評価

## Lambda 1 ダウンロード & DB 登録

### 機能概要

- `yfinance` を使用して株価データと配当金データ，為替データをダウンロード．
- 日本円建てに変換．
- PostgreSQL に格納．

### 処理フロー

1. ダウンロード対象の銘柄を取得．
2. アメリカの株価データと配当データをダウンロード．
3. 為替データをダウンロード
4. 日本円建てに変換．
5. PostgreSQL に格納．
6. 日本の株価データと配当データをダウンロード．

## Lambda 2 リターンを計算して DB に登録

### 機能概要

- 価格履歴テーブルと配当履歴テーブルのデータを使用してリターンを計算．

### 処理フロー

1. 価格履歴テーブルと配当履歴テーブルのデータを取得．
2. リターンの計算を行う．

   $$
   \begin{aligned}
   Y &= \frac{D}{250} \\
   r &= CAGR = \left( \frac{Value_f}{Value_i} \right)^{{1}/{Y}} - 1 \\
   \end{aligned}
   $$

   - r: リターン
   - CAGR: 年平均成長率 (Compound Annual Growth Rate)
   - Value_f: 最終価格
   - Value_i: 初期価格
   - Y: 年数
   - D: 日数
   - 250: 1 年当たりの取引日数

3. リターンを DB に登録．

## Lambda 3 ポートフォリオの評価

### 機能概要

- フロントから銘柄と重みを受け取る．
- 価格履歴テーブル，配当履歴テーブルからデータを取得．
- リターンの計算，リスクの計算，シャープレシオの計算を行う．

### 処理フロー

1. フロントから銘柄と重みを受け取る．
2. リターンテーブルと重みで加重平均．

   $$
   r_p = w^{\top} r
   $$

   - $w = (w_1, w_2, \cdots, w_n)^{\top}$
   - $r = (r_1, r_2, \cdots, r_n)^{\top}$

   - $r_p$: ポートフォリオのリターン
   - $w$: 重み
   - $r$: リターン

3. 価格履歴テーブルからリスクの計算を行う．

   $$
   \sigma_p^2 = w^{\top} \Sigma w
   $$

   - $w = (w_1, w_2, \cdots, w_n)^{\top}$
   - $\Sigma = \begin{pmatrix} \sigma_{11} & \sigma_{12} & \cdots & \sigma_{1n} \\ \sigma_{21} & \sigma_{22} & \cdots & \sigma_{2n} \\ \vdots & \vdots & \ddots & \vdots \\ \sigma_{n1} & \sigma_{n2} & \cdots & \sigma_{nn} \end{pmatrix}$

   - $\sigma_p$: ポートフォリオのリスク
   - $w$: 重み
   - $\Sigma$: 分散共分散行列

4. シャープレシオの計算を行う．

   $$
   S = \frac{r_p - r_f}{\sigma_p}
   $$

   - $S$: シャープレシオ
   - $r_p$: ポートフォリオのリターン
   - $r_f$: 無リスクレート．

   ※ $r_f$ には無担保コール翌日物を使用したいが，API が見つからないので今回は 0．

5. ポートフォリオの評価結果を返す．

## 参考文献

[Mathematical Finance](!http://mathfin.web.fc2.com/finan/imi_finan10.html)
