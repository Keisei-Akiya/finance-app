import polars as pl


def dividend_data_formatter(
    historical_data: pl.DataFrame,
    df_date: pl.DataFrame,
    df_exchange_rate: pl.DataFrame,
    df_investment_info: pl.DataFrame,
) -> pl.DataFrame:
    """
    配当データを整形する関数

    Parameters
    ----------
    historical_data : pl.DataFrame

    df_date : pl.DataFrame

    df_exchange_rate : pl.DataFrame

    df_investment_info : pl.DataFrame

    Returns
    -------
    df_dividends : pl.DataFrame
    """
    try:
        # 配当をpolarsのDataFrameに変換
        df_dividends_pivot: pl.DataFrame = (
            # 配当をpolarsのDataFrameに変換
            pl.DataFrame(historical_data["Dividends"])
            # 日付を追加
            .with_columns(df_date)
        )

        # ティッカーシンボルのリスト
        ticker_symbol_list: list[str] = df_investment_info.select(pl.col("ticker_symbol")).to_numpy().flatten().tolist()

        # データを長い形式に変換
        df_dividends_long: pl.DataFrame = (
            df_dividends_pivot
            # ワイド形式から長い形式に変換
            .unpivot(
                # 残すカラム
                index=["date"],
                # 変換するカラム
                on=[
                    ticker_symbol
                    for ticker_symbol in ticker_symbol_list
                    # pivotのDataFrameにティッカーシンボルが含まれている場合のみ変換
                    if ticker_symbol in df_dividends_pivot.columns
                ],
            )
            .rename({"variable": "ticker_symbol", "value": "dividends"})
            .drop_nulls()
        )

        # 配当がある場合のみ抽出
        df_dividends_not_null: pl.DataFrame = df_dividends_long.filter(pl.col("dividends") > 0)

        # 円建ての配当を計算
        df_dividends: pl.DataFrame = (
            df_dividends_not_null
            # 投資情報を結合
            .join(df_investment_info, on=["ticker_symbol"], how="left")
            # 計算のため一旦，為替レートを結合
            .join(df_exchange_rate, on=["date"], how="left")
            # 円建ての配当を計算
            .with_columns(
                # TODO 日本かどうかの判定を追加
                pl.when(pl.col("country_code") == "US")
                .then(pl.col("dividends") * pl.col("JPY=X"))
                .otherwise(pl.col("dividends"))  # 日本はそのまま
                .alias("dividends_jpy")
            )
            # 外部キー，日付，配当，円建て配当のみを残す
            .select("investment_code", "date", "dividends", "dividends_jpy")
        )

        return df_dividends

    except Exception as e:
        print(f"配当データの整形に失敗しました: {e}")
        exit()
