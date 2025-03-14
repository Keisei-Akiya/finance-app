import os

import polars as pl

# from dividend_fetcher import dividend_fetcher
from dotenv import load_dotenv
from investment_info_fetcher import investment_info_fetcher
from value_fetcher import value_fetcher


def lambda_handler() -> dict:
    try:
        # データベース接続情報
        load_dotenv()
        DB_HOST: str | None = os.getenv("DB_HOST")
        DB_PORT: str | None = os.getenv("DB_PORT")
        DB_USER: str | None = os.getenv("DB_USER")
        DB_PASSWORD: str | None = os.getenv("DB_PASSWORD")
        DB_NAME: str | None = os.getenv("DB_NAME")

        # ティッカーシンボルを取得
        ticker_symbol_list = ["VTI", "VGK", "VPL", "2561.T"]
        # `investment_info` テーブルを取得
        df_investment_info: pl.DataFrame = investment_info_fetcher(
            ticker_symbol_list, DB_HOST, DB_PORT, DB_USER, DB_PASSWORD, DB_NAME
        )

        # 投資対象のデータを取得
        df_value = value_fetcher(df_investment_info, DB_HOST, DB_PORT, DB_USER, DB_PASSWORD, DB_NAME)
        print(df_value)

        # df_dividend = dividend_fetcher(df_investment, DB_HOST, DB_PORT, DB_USER, DB_PASSWORD, DB_NAME)
        # print(df_dividend.head())

        # 重みを取得する
        # weight_list = [0.25, 0.25, 0.25, 0.25]
        #

        cagr = 0.1
        volatility = 0.2
        sharpe_ratio = cagr / volatility
        performance = {"cagr": cagr, "volatility": volatility, "sharpe_ratio": sharpe_ratio}

        return performance

    except Exception as e:
        print(f"Error: {e}")
        return {"error": str(e)}


if __name__ == "__main__":
    lambda_handler()
