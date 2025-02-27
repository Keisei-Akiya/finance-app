import polars as pl
import yfinance as yf


def exchange_rate_fetcher():
    # 為替レートを取得
    try:
        exchange_rate = yf.Ticker("JPY=X").history(period="1d")
        df_exchange_rate = (
            # 為替レートをpolarsのDataFrameに変換
            pl.DataFrame(
                {
                    "date": exchange_rate.index,
                    "JPY=X": exchange_rate["Close"].to_numpy(),
                }
            )
            # pl.Date型に変換
            .with_columns(pl.col("date").cast(pl.Date))
        )

        # date_range = pl.date_range(start_date, end_date, interval="1d").to_numpy()
        # print(date_range)
        # df_date_range = pl.DataFrame({"date": date_range})
        # df_exchange_rate = df_date_range.join(df_exchange_rate, on="date", how="left")

        # 欠損値の補完
        df_exchange_rate = (
            df_exchange_rate
            # 前日の値で欠損値を埋める
            .fill_null(strategy="forward")
        )

        print("為替レートの取得に成功しました")
        return df_exchange_rate
    except Exception as e:
        print(f"為替レートの取得に失敗しました: {e}")
        exit()
