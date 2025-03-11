import polars as pl


def investment_info_fetcher(
    DB_HOST: str | None, DB_PORT: str | None, DB_USER: str | None, DB_PASSWORD: str | None, DB_NAME: str | None
) -> pl.DataFrame:
    try:
        # 銘柄情報を取得
        select_query: list[str] | str = """
            SELECT investment_code, ticker_symbol, country_code, currency_code
            FROM public.investment_info
        """

        # TODO クエリを開発用に絞っている
        # # ランダム
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
        # select_query = """
        # SELECT investment_code, ticker_symbol, country_code, currency_code
        # FROM public.investment_info
        # WHERE country_code = 'US'
        # ORDER BY investment_info
        # LIMIT 300
        # OFFSET 300
        # """
        # OFFSETを300とすると，301から600までのデータを取得する

        uri: str = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
        df_investment_info: pl.DataFrame = pl.read_database_uri(query=select_query, uri=uri)

        return df_investment_info

    except Exception as e:
        print(f"投資コードとティッカーシンボルの取得に失敗しました: {e}")
        exit()
