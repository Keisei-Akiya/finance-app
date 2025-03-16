import polars as pl


def investment_code_fetcher(df_ticker_and_weight: pl.DataFrame, connection_config: dict[str, str]) -> pl.DataFrame:
    try:
        ticker_symbol_list: list[str] = df_ticker_and_weight["ticker_symbol"].to_list()
        # [] を外す
        ticker_symbols: str = ", ".join([f"'{ticker_symbol}'" for ticker_symbol in ticker_symbol_list])

        # polars
        select_query = f"""
        SELECT investment_code, ticker_symbol
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

        df_code_and_weight = (
            df_investment_info.join(df_ticker_and_weight, on="ticker_symbol", how="inner")
            # ticker_symbolカラムを削除
            .drop("ticker_symbol")
            # investment_code でソート
            .sort("investment_code")
        )

        return df_code_and_weight

    except Exception as e:
        print(f"投資コードとティッカーシンボルの取得に失敗しました: {e}")
        exit()
