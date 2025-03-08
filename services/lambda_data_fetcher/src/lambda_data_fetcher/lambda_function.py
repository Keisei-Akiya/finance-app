import os

import polars as pl
from dividend_data_duplicate_dropper import dividend_data_duplicate_dropper
from dividend_data_formatter import dividend_data_formatter
from dividend_data_saver import dividend_data_saver
from dotenv import load_dotenv
from exchange_rate_fetcher import exchange_rate_fetcher
from historical_data_fetcher import historical_data_fetcher
from investment_info_fetcher import investment_info_fetcher
from value_data_duplicate_dropper import value_data_duplicate_dropper
from value_data_formatter import value_data_formatter
from value_data_saver import value_data_saver


def lambda_handler() -> None:
    try:
        # PostgreSQLへの接続情報
        load_dotenv()
        DB_HOST: str | None = os.getenv("DB_HOST")
        DB_PORT: str | None = os.getenv("DB_PORT")
        DB_USER: str | None = os.getenv("DB_USER")
        DB_PASSWORD: str | None = os.getenv("DB_PASSWORD")
        DB_NAME: str | None = os.getenv("DB_NAME")

        # 為替レートを取得
        df_exchange_rate: pl.DataFrame = exchange_rate_fetcher()

        # 投資コードとティッカーシンボルを取得
        df_investment_info: pl.DataFrame = investment_info_fetcher(DB_HOST, DB_PORT, DB_USER, DB_PASSWORD, DB_NAME)

        # 投資銘柄のヒストリカルデータを取得
        historical_data: pl.DataFrame
        df_date: pl.DataFrame
        historical_data, df_date = historical_data_fetcher(df_investment_info)

        # データの整形
        df_value: pl.DataFrame = value_data_formatter(historical_data, df_date, df_exchange_rate, df_investment_info)
        df_dividend: pl.DataFrame = dividend_data_formatter(
            historical_data, df_date, df_exchange_rate, df_investment_info
        )

        # 保存
        value_data_saver(df_value, DB_HOST, DB_PORT, DB_USER, DB_PASSWORD, DB_NAME)
        dividend_data_saver(df_dividend, DB_HOST, DB_PORT, DB_USER, DB_PASSWORD, DB_NAME)

        # 重複データの削除
        value_data_duplicate_dropper(DB_HOST, DB_PORT, DB_USER, DB_PASSWORD, DB_NAME)
        dividend_data_duplicate_dropper(DB_HOST, DB_PORT, DB_USER, DB_PASSWORD, DB_NAME)

        return

    except Exception as e:
        print(f"失敗しました: {e}")
        exit()


if __name__ == "__main__":
    lambda_handler()
