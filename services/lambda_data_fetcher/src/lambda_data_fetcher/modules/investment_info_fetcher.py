import polars as pl


def investment_info_fetcher(connection_config: dict[str, str | None]) -> pl.DataFrame:
    try:
        # 銘柄情報を取得
        select_query: list[str] | str = """
            SELECT investment_code, ticker_symbol, country_code, currency_code
            FROM public.investment_info
        """

        # クエリを開発用に絞っている
        # ランダム
        # select_query = """
        # SELECT investment_code, ticker_symbol, country_code, currency_code
        # FROM public.investment_info
        # ORDER BY RANDOM() LIMIT 10
        # """

        # 日本のみ
        # select_query = """
        # SELECT investment_code, ticker_symbol, country_code, currency_code
        # FROM public.investment_info
        # WHERE country_code = 'JP'
        # """

        # アメリカのみ
        select_query = """
        SELECT investment_code, ticker_symbol, country_code, currency_code
        FROM public.investment_info
        WHERE country_code = 'US'
        ORDER BY investment_info
        LIMIT 300
        OFFSET 600
        """
        # OFFSETを300とすると，301から600までのデータを取得する

        uri: str = f"postgresql://{connection_config['user']}:{connection_config['password']}@{connection_config['host']}:{connection_config['port']}/{connection_config['dbname']}"
        df_investment_info: pl.DataFrame = pl.read_database_uri(query=select_query, uri=uri)

        return df_investment_info

    except Exception as e:
        print(f"投資コードとティッカーシンボルの取得に失敗しました: {e}")
        exit()
