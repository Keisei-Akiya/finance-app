import polars as pl


def dividend_data_formatter(
    historical_data: pl.DataFrame = None,
    df_date: pl.DataFrame = None,
    df_exchange_rate: pl.DataFrame = None,
    tickers: list = None,
):
    try:
        # 配当をpolarsのDataFrameに変換
        df_dividends_pivot = (
            # 配当をpolarsのDataFrameに変換
            pl.DataFrame(historical_data["Dividends"])
            # 日付を追加
            .with_columns(df_date)
        )

        # データを長い形式に変換
        df_dividends_long = (
            df_dividends_pivot
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

        # 配当がある場合のみ抽出
        df_dividends = df_dividends_long.filter(pl.col("dividends") > 0)

        # 円建て換算値を追加
        df_dividends = (
            df_dividends
            # 計算のため一旦，為替レートを結合
            .join(df_exchange_rate, on=["date"], how="left")
            # 円建ての配当を計算
            .with_columns((pl.col("dividends") * pl.col("JPY=X")).alias("dividends_jpy"))
            # JPY=Xの列を削除
            .drop("JPY=X")
        )
        return df_dividends
    except Exception as e:
        print(f"配当データの整形に失敗しました: {e}")
        exit()
