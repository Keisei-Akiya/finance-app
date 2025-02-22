# ライブラリのインポート
import polars as pl
import yfinance as yf

# ティッカーシンボルのリスト
tickers = ["VOO", "VGK", "JPY=X"]

# yFinance を使って株価データを取得
yf_tickers = yf.Tickers(tickers=tickers)
historical_data = yf_tickers.history(period="max")

# 日付をpolarsのDataFrameに変換
df_date = (
    pl.DataFrame(historical_data.index.to_numpy())
    .rename({"column_0": "date"})
    .with_columns(pl.col("date").cast(pl.Date))
)

# 終値をpolarsのDataFrameに変換
df_close = (
    # 終値をpolarsのDataFrameに変換
    pl.DataFrame(historical_data["Close"])
    # 日付を追加
    .with_columns(df_date)
)

# 円換算の終値を追加
expr_list = [
    # 終値に為替レートを掛け算
    ((pl.col(f"{ticker}")) * pl.col("JPY=X")).alias(f"{ticker}_JPY")
    # JPY=Xの場合はそのままの終値を使う
    if ticker != "JPY=X"
    else pl.col(f"{ticker}")
    # ティッカーシンボルのリストを使ってループ
    for ticker in tickers
]
df_close = (
    df_close
    # 終値に為替レートを掛け算
    .with_columns(expr_list)
    # JPY=Xの列を削除
    .drop("JPY=X")
    # `date` 列以外が全てnullの行を削除
    .filter(
        # 全ての行に関して `date` 列以外がnullでない
        ~pl.all_horizontal(
            pl.exclude("date").is_null(),
        )
    )
)

# データを長い形式に変換
df_close_long = (
    df_close
    # ワイド形式から長い形式に変換
    .unpivot(
        # 残すカラム
        index=["date"],
        # 変換するカラム
        on=[ticker for ticker in tickers if ticker != "JPY=X"],
    )
    .rename({"variable": "ticker", "value": "value"})
    .drop_nulls()
)

# 円換算の終値を追加
df_close_jpy_long = (
    # ワイド形式から長い形式に変換
    df_close.unpivot(
        # 残すカラム
        index=["date"],
        # 変換するカラム
        on=[f"{ticker}_JPY" for ticker in tickers if ticker != "JPY=X"],
    )
    .rename({"variable": "ticker_jpy", "value": "value_jpy"})
    .drop_nulls()
)

# 結合
df_final = (
    df_close_long
    # 円建ての終値を結合
    .join(df_close_jpy_long, on=["date"], how="left")
    # 円建てのティッカーシンボルを削除
    .drop("ticker_jpy")
)

# print(df_final.head())

# 配当を円換算するために為替レートと日付を取り出す
df_exchange_rate_and_date = (
    # 為替レートをpolarsのDataFrameに変換
    pl.DataFrame(historical_data["Close"]["JPY=X"].to_numpy())
    .rename({"column_0": "JPY=X"})
    # 日付を追加
    .with_columns(df_date)
)

# 配当をpolarsのDataFrameに変換
df_dividends = (
    # 配当をpolarsのDataFrameに変換
    pl.DataFrame(historical_data["Dividends"])
    # 為替レートと日付を追加
    .with_columns(df_exchange_rate_and_date)
)

# 円換算の配当を追加
expr_list = [
    # 配当に為替レートを掛け算
    ((pl.col(f"{ticker}")) * pl.col("JPY=X")).alias(f"{ticker}_JPY")
    # JPY=Xの場合はそのままの配当を使う
    if ticker != "JPY=X"
    else pl.col(f"{ticker}")
    # ティッカーシンボルのリストを使ってループ
    for ticker in tickers
]

df_dividends = (
    df_dividends
    # 配当に為替レートを掛け算
    .with_columns(expr_list)
    # JPY=Xの列を削除
    .drop("JPY=X")
)

df_dividends_long = (
    df_dividends
    # ワイド形式から長い形式に変換
    .unpivot(
        # 残すカラム
        index=["date"],
        # 変換するカラム
        on=[ticker for ticker in tickers if ticker != "JPY=X"],
    )
    .rename({"variable": "ticker", "value": "value"})
    .drop_nulls()
)

df_dividends_jpy_long = (
    # ワイド形式から長い形式に変換
    df_dividends.unpivot(
        # 残すカラム
        index=["date"],
        # 変換するカラム
        on=[f"{ticker}_JPY" for ticker in tickers if ticker != "JPY=X"],
    )
    .rename({"variable": "ticker_jpy", "value": "value_jpy"})
    .drop_nulls()
)

df_dividends_final = (
    df_dividends_long
    # 円建ての配当を結合
    .join(df_dividends_jpy_long, on=["date"], how="left")
    # 円建てのティッカーシンボルを削除
    .drop("ticker_jpy")
)

print(df_dividends_final.head())
