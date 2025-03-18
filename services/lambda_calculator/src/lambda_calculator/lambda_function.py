import numpy as np
import pandas as pd
import polars as pl
from cagr_calculator import calculate_cagr
from dividend_fetcher import dividend_fetcher
from get_connection_config import get_connection_config
from investment_code_fetcher import investment_code_fetcher
from json_to_dataframe import json_to_dataframe
from value_fetcher import value_fetcher
from volatility_calculator import calculate_volatility


def lambda_handler() -> str:
    try:
        # データベース接続情報を取得
        connection_config = get_connection_config()

        # TODO リクエストからティッカーシンボルとウェイトを取得
        df_ticker_and_weights: pl.DataFrame = json_to_dataframe()

        # `investment_info` テーブルを取得
        df_code_and_weights: pl.DataFrame = investment_code_fetcher(df_ticker_and_weights, connection_config)

        # 投資対象のデータを取得
        df_value: pl.DataFrame = value_fetcher(df_code_and_weights, connection_config)

        df_dividend: pl.DataFrame = dividend_fetcher(df_code_and_weights, connection_config)

        # パフォーマンス計算
        # 1年あたりの取引日数
        TRADING_DAYS_PER_YEAR = 252

        # リターン (CAGR)
        cagr_array: np.ndarray = calculate_cagr(df_code_and_weights, df_value, df_dividend, TRADING_DAYS_PER_YEAR)

        # ボラティリティ
        volatility_array: np.ndarray = calculate_volatility(df_code_and_weights, df_value, TRADING_DAYS_PER_YEAR)

        # シャープレシオ
        rf = 0  # リスクフリーレートは0とする
        sharpe_ratio_array: np.ndarray = (cagr_array - rf) / volatility_array

        # 返却用にパフォーマンスをPandasにまとめる
        df_performance: pd.DataFrame = pd.DataFrame(
            {
                "pf_id": [1, 2, 3],
                "cagr": cagr_array,
                "volatility": volatility_array,
                "sharpe_ratio": sharpe_ratio_array,
            }
        )

        # jsonに変換
        json_performance: str = df_performance.to_json()

        return json_performance

    except Exception as e:
        print(f"Error: {e}")
        exit()


if __name__ == "__main__":
    lambda_handler()
