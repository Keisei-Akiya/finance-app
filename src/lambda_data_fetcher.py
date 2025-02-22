# ライブラリのインポート
import polars as pl
import yfinance as yf

# 為替レートを取得
exchange_rate = yf.Ticker("JPY=X").history(period="max")
df_exchange_rate = pl.DataFrame(
    {
        "date": exchange_rate.index,
        "JPY=X": exchange_rate["Close"].to_numpy(),
    }
).with_columns(pl.col("date").cast(pl.Date))

# 履歴データを取得
# ティッカーシンボルのリスト
tickers: list = ["VOO", "VGK"]
# yFinance を使って株価データを取得
yf_tickers = yf.Tickers(tickers=tickers)
historical_data = yf_tickers.history(period="max")

# 日付をpolarsのDataFrameに変換
df_date = (
    pl.DataFrame(historical_data.index.to_numpy())
    .rename({"column_0": "date"})
    .with_columns(pl.col("date").cast(pl.Date))
)


# 終値
# 終値をpolarsのDataFrameに変換
df_close = (
    # 終値をpolarsのDataFrameに変換
    pl.DataFrame(historical_data["Close"])
    # 日付を追加
    .with_columns(df_date)
)

# データを長い形式に変換
df_close_long = (
    df_close
    # ワイド形式から長い形式に変換
    .unpivot(
        # 残すカラム
        index=["date"],
        # 変換するカラム
        on=[ticker for ticker in tickers],
    )
    .rename({"variable": "ticker", "value": "value"})
    .drop_nulls()
)

# 円建て換算
df_close_long = (
    df_close_long
    # 為替レートを結合
    .join(df_exchange_rate, on=["date"], how="left")
    # 円建ての終値を計算
    .with_columns((pl.col("value") * pl.col("JPY=X")).alias("value_jpy"))
    # JPY=Xの列を削除
    .drop("JPY=X")
)


# 配当
# 配当をpolarsのDataFrameに変換
df_dividends = (
    # 配当をpolarsのDataFrameに変換
    pl.DataFrame(historical_data["Dividends"])
    # 日付を追加
    .with_columns(df_date)
)


# データを長い形式に変換
df_dividends_long = (
    df_dividends
    # ワイド形式から長い形式に変換
    .unpivot(
        # 残すカラム
        index=["date"],
        # 変換するカラム
        on=[ticker for ticker in tickers if ticker != "JPY=X"],
    )
    .rename({"variable": "ticker", "value": "dividends"})
    .drop_nulls()
)

# 円建て換算
df_dividends_long = (
    df_dividends_long
    # 為替レートを結合
    .join(df_exchange_rate, on=["date"], how="left")
    # 円建ての配当を計算
    .with_columns((pl.col("dividends") * pl.col("JPY=X")).alias("dividends_jpy"))
    # JPY=Xの列を削除
    .drop("JPY=X")
)
