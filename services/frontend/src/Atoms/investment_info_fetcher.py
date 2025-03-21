import os

import polars as pl
import psycopg2
import psycopg2._psycopg
import streamlit as st
from dotenv import load_dotenv


def fetch_investment_info() -> pl.DataFrame:
    try:
        # SQL クエリ
        select_query = """
        SELECT investment_code, ticker_symbol, investment_name
        FROM investment_info
        """
        # DB 接続情報を取得
        load_dotenv()
        config: dict[str, str | None] = {
            "host": os.getenv("DB_HOST"),
            "port": os.getenv("DB_PORT"),
            "user": os.getenv("DB_USER"),
            "password": os.getenv("DB_PASSWORD"),
            "dbname": os.getenv("DB_NAME"),
        }

        # DB 接続
        conn: psycopg2._psycopg.connection = psycopg2.connect(**config)

        df: pl.DataFrame = (
            # DB からデータを取得
            pl.read_database(query=select_query, connection=conn)
            # ティッカーと名前を合体させたカラムを作成
            .with_columns((pl.col("ticker_symbol") + " " + pl.col("investment_name")).alias("ticker_and_name"))
        )

        return df

    except Exception as e:
        st.write(e)
        exit()

    finally:
        # DB 接続を閉じる
        conn.close()
