import polars as pl


def value_fetcher(
    df_investment_info: pl.DataFrame,
    DB_HOST: str | None,
    DB_PORT: str | None,
    DB_USER: str | None,
    DB_PASSWORD: str | None,
    DB_NAME: str | None,
) -> pl.DataFrame:
    try:
        # 文字列型に変換した投資コードのリストを作成
        investment_code_list: str = ",".join(
            [f"'{investment_code}'" for investment_code in df_investment_info["investment_code"].to_list()]
        )

        select_query = f"""
        SELECT *
        FROM public.value_history
        WHERE investment_code IN ({investment_code_list})
        """

        # データベース接続
        uri = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
        print("26")
        df_value: pl.DataFrame = pl.DataFrame()
        df_value: pl.DataFrame = pl.read_database_uri(
            query=select_query,
            uri=uri,
        )
        print("31")

        return df_value

    except Exception as e:
        print(f"投資対象のデータの取得に失敗しました: {e}")
        exit()
