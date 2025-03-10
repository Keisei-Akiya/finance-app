import polars as pl


def ticker_filter(df_investment_info: pl.DataFrame, ticker_symbol_list: list[str]) -> pl.DataFrame:
    try:
        # ティッカーシンボルをフィルタリング
        df_investment = (
            df_investment_info
            # フィルタリング
            .filter(pl.col("ticker_symbol").is_in(ticker_symbol_list))
            # investment_code と ticker_symbol のみ取得
            .select(pl.col("investment_code", "ticker_symbol"))
        )

        return df_investment

    except Exception as e:
        print(f"ティッカーシンボルのフィルタリングに失敗しました: {e}")
        exit()
