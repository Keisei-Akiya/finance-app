import pandas as pd
import polars as pl
from sqlalchemy import create_engine


def value_fetcher(df_investment_info: pl.DataFrame, connection_config: dict[str, str]) -> pl.DataFrame:
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

        # データベース接続
        uri = f"postgresql://{connection_config['user']}:{connection_config['password']}@{connection_config['host']}:{connection_config['port']}/{connection_config['dbname']}"
        engine = create_engine(uri)

        # Pandas DataFrame に変換
        df_value_pd: pd.DataFrame = pd.read_sql_query(select_query, engine)
        df_value_pd["investment_code"] = df_value_pd["investment_code"].astype(str)
        df_value: pl.DataFrame = pl.DataFrame(df_value_pd)

        return df_value

    except Exception as e:
        print(f"投資対象のデータの取得に失敗しました: {e}")
        exit()
