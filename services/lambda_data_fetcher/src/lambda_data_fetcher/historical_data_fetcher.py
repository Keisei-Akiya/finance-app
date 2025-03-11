import time

import pandas as pd
import polars as pl
import yfinance as yf


# データを取得
def historical_data_fetcher(df_investment_info: pl.DataFrame) -> tuple[pl.DataFrame, pl.DataFrame]:
    try:
        # ティッカーシンボルのリスト
        ticker_symbol_list: list[str] = df_investment_info.select(pl.col("ticker_symbol")).to_numpy().flatten().tolist()

        # 分割してリクエスト
        chunk_size: int = 10
        historical_dataframe_list: list[pd.DataFrame] = []

        # ティッカーシンボルをchunk_sizeごとに分割してリクエスト
        for i in range(0, len(ticker_symbol_list), chunk_size):
            chunk: list[str] = ticker_symbol_list[i : i + chunk_size]
            yf_tickers = yf.Tickers(tickers=chunk)

            try:
                # TODO 期間を変更する
                historical_data_chunk: pd.DataFrame = yf_tickers.history(period="max")[["Close", "Dividends"]]
                # データをリストに追加
                historical_dataframe_list.append(historical_data_chunk)
                # 1秒待機
                time.sleep(1)

            except Exception as e:
                print(f"データの取得に失敗しました: {e}")
                # 30秒待機
                time.sleep(30)

        # データを結合
        historical_data: pd.DataFrame = pd.concat(
            historical_dataframe_list,
            axis=1,  # こうしないと date列が重複してしまう
        )

        # 価格データをpolarsのDataFrameに変換
        df_value_pivot = (
            pl.DataFrame(historical_data["Close"].reset_index())
            .with_columns(pl.col("Date").cast(pl.Date))
            .rename({"Date": "date"})
        )

        # 配当データをpolarsのDataFrameに変換
        df_dividend_pivot = (
            pl.DataFrame(historical_data["Dividends"].reset_index())
            .with_columns(pl.col("Date").cast(pl.Date))
            .rename({"Date": "date"})
        )

        print("データの取得に成功しました")
        return df_value_pivot, df_dividend_pivot

    except Exception as e:
        print(f"データの取得に失敗しました: {e}")
        exit()
