import polars as pl


def investment_info_fetcher(
    ticker_symbol_list: list[str],
    DB_HOST: str | None,
    DB_PORT: str | None,
    DB_USER: str | None,
    DB_PASSWORD: str | None,
    DB_NAME: str | None,
) -> pl.DataFrame:
    try:
        ticker_symbols: str = ", ".join([f"'{ticker_symbol}'" for ticker_symbol in ticker_symbol_list])

        # polars
        select_query = f"""
        SELECT investment_code, ticker_symbol, investment_name
        FROM public.investment_info
        WHERE ticker_symbol IN ({ticker_symbols})
        """

        uri = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
        df_investment_info: pl.DataFrame = pl.read_database_uri(
            query=select_query,
            uri=uri,
        )

        return df_investment_info

    except Exception as e:
        print(f"投資コードとティッカーシンボルの取得に失敗しました: {e}")
        exit()
