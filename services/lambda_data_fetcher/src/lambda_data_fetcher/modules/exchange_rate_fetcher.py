import pandas as pd
import polars as pl
import yfinance as yf


def exchange_rate_fetcher() -> pl.DataFrame:
    try:
        # 為替レートを取得
        # 期間を一週間に変更する (1wk)
        exchange_rate: pd.DataFrame = yf.Ticker("JPY=X").history(period="1wk")["Close"]

        # 為替レートをpolarsのDataFrameに変換
        df_exchange_rate_pl: pl.DataFrame = (
            pl.DataFrame(exchange_rate.reset_index())
            .rename({"Date": "date", "Close": "JPY=X"})
            .with_columns(pl.col("date").cast(pl.Date))
        )

        print("為替レートの取得に成功しました")

        # 日付を生成 (`exchange_rate`は営業日のみのデータ故に日本の土日は含まれていないため．)
        start_date = df_exchange_rate_pl["date"].min()
        end_date = df_exchange_rate_pl["date"].max()
        date_range: pd.DatetimeIndex = pd.date_range(start=start_date, end=end_date, freq="D")

        # 日付をpolarsのDataFrameに変換
        df_date_range: pl.DataFrame = (
            pl.DataFrame(date_range.to_numpy())
            # 名前を付ける
            .rename({"column_0": "date"})
            # 日付型に変換
            .with_columns(pl.col("date").cast(pl.Date))
        )

        # 日付を結合して欠損値を埋める
        df_exchange_rate: pl.DataFrame = (
            # 日付を結合
            df_date_range.join(df_exchange_rate_pl, on="date", how="left")
            # 欠損値を前日の値で埋める
            .fill_null(strategy="forward")
        )

        print("為替レートの欠損値の補完に成功しました")

        return df_exchange_rate

    except Exception as e:
        print(f"為替レートの取得に失敗しました: {e}")
        exit()
