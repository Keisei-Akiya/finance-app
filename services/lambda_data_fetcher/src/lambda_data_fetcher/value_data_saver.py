import os

import polars as pl
from dotenv import load_dotenv


def value_data_saver(df_value: pl.DataFrame) -> None:
    try:
        # 環境変数を読み込む
        load_dotenv()

        # 環境変数からPostgreSQLの接続情報を取得
        DB_HOST = os.getenv("DB_HOST")
        DB_PORT = os.getenv("DB_PORT")
        DB_NAME = os.getenv("DB_NAME")
        DB_USER = os.getenv("DB_USER")
        DB_PASSWORD = os.getenv("DB_PASSWORD")

        df_value.write_database(
            table_name="value_history",
            connection=f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}",
            if_table_exists="append", # 重複データが生まれる可能性がある．
            engine="sqlalchemy",
        )
        print("価格データを保存しました")

    except Exception as e:
        print(f"価格データの保存に失敗しました: {e}")
