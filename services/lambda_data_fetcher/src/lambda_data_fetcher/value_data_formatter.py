import polars as pl


def value_data_formatter(
    df_value_pivot: pl.DataFrame,
    df_exchange_rate: pl.DataFrame,
    df_investment_info: pl.DataFrame,
) -> pl.DataFrame:
    """_summary_

    Parameters
    ----------
    df_value_pivot : pl.DataFrame
        _summary_
    df_exchange_rate : pl.DataFrame
        _summary_
    df_investment_info : pl.DataFrame
        _summary_

    Returns
    -------
    pl.DataFrame
        _summary_

    """
    try:
        # ティッカーシンボルのリスト
        ticker_symbol_list: list[str] = df_investment_info.select(pl.col("ticker_symbol")).to_numpy().flatten().tolist()

        # データをDB用の長い形式に変換
        df_value_long: pl.DataFrame = (
            df_value_pivot
            # ワイド形式から長い形式に変換
            .unpivot(
                # 残すカラム
                index=["date"],
                # 変換するカラム
                on=[
                    ticker_symbol
                    for ticker_symbol in ticker_symbol_list
                    # pivotのDataFrameにティッカーシンボルが含まれている場合のみ変換
                    if ticker_symbol in df_value_pivot.columns
                ],
            )
            .rename({"variable": "ticker_symbol", "value": "value"})
            .drop_nulls()
        )

        # 円建て換算値を追加
        df_value: pl.DataFrame = (
            df_value_long
            # 計算のため為替レートを結合
            .join(df_exchange_rate, on=["date"], how="left")
            # 通貨分けのため投資情報を結合
            .join(df_investment_info, on="ticker_symbol", how="left")
            # 円建ての終値を計算
            .with_columns(
                # USDの場合は為替レートをかける
                pl.when(pl.col("currency_code") == "USD")
                .then(
                    # 終値 * 為替レート
                    (pl.col("value") * pl.col("JPY=X"))
                    # NUMERIC型の制約のため丸める
                    .round(2)
                )
                # 日本はそのまま
                .otherwise(pl.col("value").round(2))
                .alias("value_jpy")
            )
            # 外部キーと日付，価格，円建て価格のみを残す
            .select("investment_code", "date", "value", "value_jpy")
        )

        return df_value

    except Exception as e:
        print(f"価格データの整形に失敗しました: {e}")
        exit()
