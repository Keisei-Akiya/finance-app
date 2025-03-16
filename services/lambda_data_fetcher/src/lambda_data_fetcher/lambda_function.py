import os

import polars as pl
import psycopg2
import psycopg2._psycopg
from dividend_data_formatter import dividend_data_formatter
from dividend_data_saver import dividend_data_saver
from dotenv import load_dotenv
from exchange_rate_fetcher import exchange_rate_fetcher
from historical_data_fetcher import historical_data_fetcher
from investment_info_fetcher import investment_info_fetcher
from value_data_formatter import value_data_formatter
from value_data_saver import value_data_saver


def lambda_handler() -> None:
    try:
        # PostgreSQLへの接続情報
        load_dotenv()
        connection_config: dict[str, str | None] = {
            "dbname": os.getenv("DB_NAME"),
            "user": os.getenv("DB_USER"),
            "password": os.getenv("DB_PASSWORD"),
            "host": os.getenv("DB_HOST"),
            "port": os.getenv("DB_PORT"),
        }

        # データベースへの接続
        conn: psycopg2._psycopg.connection = psycopg2.connect(**connection_config)

        # 為替レートを取得
        # 日次
        df_exchange_rate: pl.DataFrame = exchange_rate_fetcher()

        # 投資コードとティッカーシンボルを取得
        df_investment_info: pl.DataFrame = investment_info_fetcher(connection_config)

        # 投資銘柄のヒストリカルデータを取得
        df_value_pivot: pl.DataFrame
        df_dividend_pivot: pl.DataFrame
        df_value_pivot, df_dividend_pivot = historical_data_fetcher(df_investment_info)

        # データの整形
        df_value: pl.DataFrame = value_data_formatter(df_value_pivot, df_exchange_rate, df_investment_info)
        df_dividend: pl.DataFrame = dividend_data_formatter(df_dividend_pivot, df_exchange_rate, df_investment_info)

        # 保存
        value_data_saver(conn, df_value)
        dividend_data_saver(conn, df_dividend)

    except Exception as e:
        print(f"失敗しました: {e}")
        exit()

    finally:
        conn.close()


if __name__ == "__main__":
    lambda_handler()
