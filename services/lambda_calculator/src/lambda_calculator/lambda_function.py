import numpy as np
import polars as pl
from cagr_calculator import calculate_cagr
from dividend_fetcher import dividend_fetcher
from get_connection_config import get_connection_config
from investment_code_fetcher import investment_code_fetcher
from json_to_dataframe import json_to_dataframe
from value_fetcher import value_fetcher
from volatility_calculator import calculate_volatility


def lambda_handler() -> pl.DataFrame:
    try:
        # データベース接続情報を取得
        connection_config = get_connection_config()

        # TODO ティッカーシンボルを取得
        df_ticker_and_weights: pl.DataFrame = json_to_dataframe()

        # `investment_info` テーブルを取得
        df_code_and_weights: pl.DataFrame = investment_code_fetcher(df_ticker_and_weights, connection_config)
        # print(df_investment_info)

        # 投資対象のデータを取得
        df_value: pl.DataFrame = value_fetcher(df_code_and_weights, connection_config)
        # print(df_value)

        df_dividend: pl.DataFrame = dividend_fetcher(df_code_and_weights, connection_config)
        # print(df_dividend.head())

        # パフォーマンス計算
        TRADING_DAYS_PER_YEAR = 252

        # リターン (CAGR)
        cagr_array: np.ndarray = calculate_cagr(df_ticker_and_weights, df_value, df_dividend, TRADING_DAYS_PER_YEAR)

        # ボラティリティ
        volatility_array: np.ndarray = calculate_volatility(df_code_and_weights, df_value, TRADING_DAYS_PER_YEAR)

        # シャープレシオ
        sharpe_ratio_array: np.ndarray = cagr_array / volatility_array

        # パフォーマンスをまとめる
        performance: pl.DataFrame = pl.DataFrame(
            {
                "pf_id": [1, 2, 3],
                "cagr": cagr_array,
                "volatility": volatility_array,
                "sharpe_ratio": sharpe_ratio_array,
            }
        )

        print(performance)

        return performance

    except Exception as e:
        print(f"Error: {e}")
        exit()


if __name__ == "__main__":
    lambda_handler()
