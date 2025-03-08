import pandas as pd
import polars as pl
import yfinance as yf


# データを取得
def historical_data_fetcher(df_investment_info: pl.DataFrame) -> tuple[pl.DataFrame, pl.DataFrame]:
    try:
        # ティッカーシンボルのリスト
        ticker_symbol_list: list[str] = df_investment_info.select(pl.col("ticker_symbol")).to_numpy().flatten().tolist()
        # yFinance を使って株価データを取得
        yf_tickers = yf.Tickers(tickers=ticker_symbol_list)
        historical_data: pd.DataFrame = yf_tickers.history(period="1d")

        # 日付をpolarsのDataFrameに変換
        # 2つの戻り値があるのは，仕方ない．
        df_date: pl.DataFrame = (
            pl.DataFrame(historical_data.index.to_numpy())
            .rename({"column_0": "date"})
            .with_columns(pl.col("date").cast(pl.Date))
        )

        print("データの取得に成功しました")
        return historical_data, df_date

    except Exception as e:
        print(f"データの取得に失敗しました: {e}")
        exit()
