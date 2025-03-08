import polars as pl


def dividend_data_formatter(
    historical_data: pl.DataFrame,
    df_date: pl.DataFrame,
    df_exchange_rate: pl.DataFrame,
    investment_code_list: list[str],
    ticker_symbol_list: list[str]
) -> pl.DataFrame:
    """
    配当データを整形する関数

    Parameters
    ----------
    historical_data : pl.DataFrame

    df_date : pl.DataFrame

    df_exchange_rate : pl.DataFrame

    tickers : list[str]

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

        # データを長い形式に変換
        df_dividends_long: pl.DataFrame = (
            df_dividends_pivot
            # ワイド形式から長い形式に変換
            .unpivot(
                # 残すカラム
                index=["date"],
                # 変換するカラム
                on=[
                    ticker_symbol for ticker_symbol in ticker_symbol_list
                    # pivotのDataFrameにティッカーシンボルが含まれている場合のみ変換
                    if ticker_symbol in df_dividends_pivot.columns
                ]
            )
            .rename({"variable": "ticker_symbol", "value": "dividends"})
            .drop_nulls()
        )

        # 配当がある場合のみ抽出
        df_dividends_not_null: pl.DataFrame = df_dividends_long.filter(pl.col("dividends") > 0)

        # 円建て換算値を追加
        df_dividends_contains_jpy: pl.DataFrame = (
            df_dividends_not_null
            # 計算のため一旦，為替レートを結合
            .join(df_exchange_rate, on=["date"], how="left")
            # 円建ての配当を計算
            .with_columns(
                # TODO 日本かどうかの判定を追加
                (pl.col("dividends") * pl.col("JPY=X")).alias("dividends_jpy")
            )
            # 為替レート `JPY=X` を削除
            .drop("JPY=X")
        )

        # ティッカーシンボルを投資コードに変換
        symbol_and_code_dict: dict[str, str] = {
            ticker_symbol_list[i]: investment_code_list[i] for i in range(len(ticker_symbol_list))
        }
        df_dividends = (
            df_dividends_contains_jpy
            .with_columns(
                pl.when(pl.col('ticker_symbol').is_in(ticker_symbol_list))
                # 辞書に従って置き換える
                .then(pl.col('ticker_symbol').replace(symbol_and_code_dict, default=None))
                .alias("investment_code")
            )
            .drop("ticker_symbol")
        )

        return df_dividends

    except Exception as e:
        print(f"配当データの整形に失敗しました: {e}")
        exit()
