import polars as pl


def value_fetcher(df_investment_info: pl.DataFrame, connection_config: dict[str, str]) -> pl.DataFrame:
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
        DB_HOST = connection_config["host"]
        DB_PORT = connection_config["port"]
        DB_USER = connection_config["user"]
        DB_PASSWORD = connection_config["password"]
        DB_NAME = connection_config["dbname"]

        uri = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
        print("26")
        df_value: pl.DataFrame = pl.read_database_uri(
            query=select_query,
            uri=uri,
        )
        print("31")

        return df_value

    except Exception as e:
        print(f"投資対象のデータの取得に失敗しました: {e}")
        exit()
