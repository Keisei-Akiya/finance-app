import polars as pl


def investment_info_fetcher(
    DB_HOST: str | None, DB_PORT: str | None, DB_USER: str | None, DB_PASSWORD: str | None, DB_NAME: str | None
) -> pl.DataFrame:
    try:
        # polars
        uri = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
        query = "SELECT investment_code, ticker_symbol, country_code FROM public.investment_info"
        df_investment_info: pl.DataFrame = pl.read_database_uri(query=query, uri=uri)

        return df_investment_info

    except Exception as e:
        print(f"投資コードとティッカーシンボルの取得に失敗しました: {e}")
        exit()
