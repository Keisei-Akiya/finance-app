import polars as pl


def value_data_formatter(
    historical_data: pl.DataFrame = None,
    df_date: pl.DataFrame = None,
    df_exchange_rate: pl.DataFrame = None,
    tickers: list = None,
):
    try:
        # 終値をpolarsのDataFrameに変換
        df_value_pivot = (
            # 終値をpolarsのDataFrameに変換
            pl.DataFrame(historical_data["Close"])
            # 日付を追加
            .with_columns(df_date)
        )

        # データを長い形式に変換
        df_value = (
            df_value_pivot
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

        # 円建て換算値を追加
        df_value = (
            df_value
            # 計算のため一旦，為替レートを結合
            .join(df_exchange_rate, on=["date"], how="left")
            # 円建ての終値を計算
            .with_columns((pl.col("value") * pl.col("JPY=X")).alias("value_jpy"))
            # JPY=Xの列を削除
            .drop("JPY=X")
        )
        return df_value

    except Exception as e:
        print(f"価格データの整形に失敗しました: {e}")
        exit()
