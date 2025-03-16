import polars as pl


def investment_info_fetcher(ticker_symbol_list: list[str], connection_config: dict[str, str]) -> pl.DataFrame:
    try:
        ticker_symbols: str = ", ".join([f"'{ticker_symbol}'" for ticker_symbol in ticker_symbol_list])

        # polars
        select_query = f"""
        SELECT investment_code, ticker_symbol, investment_name
        FROM public.investment_info
        WHERE ticker_symbol IN ({ticker_symbols})
        """

        # データベース接続
        DB_HOST = connection_config["host"]
        DB_PORT = connection_config["port"]
        DB_USER = connection_config["user"]
        DB_PASSWORD = connection_config["password"]
        DB_NAME = connection_config["dbname"]

        uri = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
        df_investment_info: pl.DataFrame = pl.read_database_uri(
            query=select_query,
            uri=uri,
        )

        return df_investment_info

    except Exception as e:
        print(f"投資コードとティッカーシンボルの取得に失敗しました: {e}")
        exit()
