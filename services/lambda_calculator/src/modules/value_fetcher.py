import polars as pl
import psycopg2
import psycopg2._psycopg


def value_fetcher(df_investment_info: pl.DataFrame, conn: psycopg2._psycopg.connection) -> pl.DataFrame:
    try:
        # 文字列型に変換した投資コードのリストを作成
        investment_code_list: str = ",".join(
            [f"'{investment_code}'" for investment_code in df_investment_info["investment_code"].to_list()]
        )

        # SQLクエリ (投資対象のデータを取得)
        select_query: str = f"""
        SELECT *
        FROM public.value_history
        WHERE investment_code IN ({investment_code_list})
        """

        # DB接続
        df_value = pl.read_database(query=select_query, connection=conn)

        return df_value

    except Exception as e:
        print(f"投資対象のデータの取得に失敗しました: {e}")
        exit()
