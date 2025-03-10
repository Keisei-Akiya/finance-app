import polars as pl


def value_fetcher(
    df_investment: pl.DataFrame,
    DB_HOST: str | None,
    DB_PORT: str | None,
    DB_USER: str | None,
    DB_PASSWORD: str | None,
    DB_NAME: str | None,
) -> pl.DataFrame:
    try:
        investment_code_list = df_investment["investment_code"].to_list()
        print(investment_code_list)

        # データベース接続
        uri = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
        # investment_code = investment_code_list[0]
        # query = f"SELECT * FROM public.value_history WHERE investment_code = '{investment_code}';"
        query = "SELECT * FROM public.value_history"
        df_value: pl.DataFrame = pl.read_database_uri(query, uri)

        return df_value

    except Exception as e:
        print(f"投資対象のデータの取得に失敗しました: {e}")
        exit()
