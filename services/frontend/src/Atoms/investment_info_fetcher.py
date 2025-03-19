import os

import pandas as pd
import polars as pl
import streamlit as st
from dotenv import load_dotenv
from sqlalchemy import create_engine


def fetch_investment_info() -> pd.DataFrame:
    try:
        # SQL クエリ
        select_query = """
        SELECT investment_code, ticker_symbol, investment_name
        FROM investment_info
        """
        # DB 接続情報を取得
        load_dotenv()
        connection_config = {
            "host": os.getenv("DB_HOST"),
            "port": os.getenv("DB_PORT"),
            "user": os.getenv("DB_USER"),
            "password": os.getenv("DB_PASSWORD"),
            "dbname": os.getenv("DB_NAME"),
        }
        # DB 接続
        uri = f"postgresql://{connection_config['user']}:{connection_config['password']}@{connection_config['host']}:{connection_config['port']}/{connection_config['dbname']}"
        engine = create_engine(uri)
        df_pd: pd.DateOffset = pd.read_sql_query(select_query, engine)
        df_pd["investment_code"] = df_pd["investment_code"].astype(str)
        df: pl.DataFrame = (
            # Pandas DataFrame を Polars DataFrame に変換
            pl.DataFrame(df_pd)
            # ティッカーと名前を合体させたカラムを作成
            .with_columns((pl.col("ticker_symbol") + " " + pl.col("investment_name")).alias("ticker_and_name"))
        )

        return df

    except Exception as e:
        st.write(e)
        exit()
