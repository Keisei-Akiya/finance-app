import os

import polars as pl
import psycopg2
from dividend_data_formatter import dividend_data_formatter

# from dividend_data_saver import dividend_data_saver
from dotenv import load_dotenv
from exchange_rate_fetcher import exchange_rate_fetcher
from historical_data_fetcher import historical_data_fetcher
from ticker_and_investment_code_fetcher import ticker_and_investment_code_fetcher
from value_data_formatter import value_data_formatter

# from value_data_saver import value_data_saver


def lambda_handler() -> None:
    try:
        # 環境変数を読み込む
        env_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), ".env")
        load_dotenv(dotenv_path=env_path)

        # 環境変数からPostgreSQLの接続情報を取得
        DB_HOST = os.getenv("DB_HOST")
        DB_PORT = os.getenv("DB_PORT")
        DB_NAME = os.getenv("DB_NAME")
        DB_USER = os.getenv("DB_USER")
        DB_PASSWORD = os.getenv("DB_PASSWORD")

        # PostgreSQLに接続
        conn: psycopg2.connection = psycopg2.connect(
            host=DB_HOST, port=DB_PORT, dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD
        )
        print("PostgreSQLへの接続に成功しました")

        # 為替レートを取得
        df_exchange_rate: pl.DataFrame = exchange_rate_fetcher()

        # TODO ティッカーシンボルと `investment_code` を取得
        ticker_list: list[str]
        investment_code_list: list[str]
        ticker_list, investment_code_list = ticker_and_investment_code_fetcher()

        # 投資銘柄のヒストリカルデータを取得
        historical_data: pl.DataFrame
        df_date: pl.DataFrame
        historical_data, df_date = historical_data_fetcher(ticker_list=ticker_list)

        # 価格履歴データを整える
        df_value: pl.DataFrame = value_data_formatter(
            historical_data=historical_data, df_date=df_date, df_exchange_rate=df_exchange_rate, tickers=ticker_list
        )
        print(df_value.head())
        # TODO 価格履歴データをPostgreSQLに保存
        # value_data_saver(df_value)

        # 配当データを整える
        df_dividend: pl.DataFrame = dividend_data_formatter(
            historical_data=historical_data, df_date=df_date, df_exchange_rate=df_exchange_rate, tickers=ticker_list
        )
        print(df_dividend.head())
        # TODO 配当データをPostgreSQLに保存
        # dividend_data_saver(df_dividend)
        return

    except Exception as e:
        print(f"失敗しました: {e}")
        exit()

    finally:
        # PostgreSQLとの接続を切断
        conn.close()


if __name__ == "__main__":
    lambda_handler()
