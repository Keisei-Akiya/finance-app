import numpy as np
import polars as pl

from modules.cagr_calculator import calculate_cagr
from modules.volatility_calculator import calculate_volatility


def calculate_performance(
    df_code_and_weights: pl.DataFrame, df_value: pl.DataFrame, df_dividend: pl.DataFrame, TRADING_DAYS_PER_YEAR: int
) -> str:
    try:
        # パフォーマンス計算
        # リターン (CAGR)
        cagr_array: np.ndarray = calculate_cagr(df_code_and_weights, df_value, df_dividend, TRADING_DAYS_PER_YEAR)

        # ボラティリティ
        volatility_array: np.ndarray = calculate_volatility(df_code_and_weights, df_value, TRADING_DAYS_PER_YEAR)

        # シャープレシオ
        rf = 0  # リスクフリーレートは0とする
        sharpe_ratio_array: np.ndarray = (cagr_array - rf) / volatility_array

        # 返却用にパフォーマンスをPandasにまとめる
        df_performance: pl.DataFrame = pl.DataFrame(
            {
                "pf_id": [1, 2, 3],
                "return": np.round(cagr_array, 2),
                "volatility": np.round(volatility_array, 2),
                "sharpe_ratio": np.round(sharpe_ratio_array, 2),
            }
        )

        # JSON
        json_performance: str = df_performance.write_json()

        return json_performance

    except Exception as e:
        print(f"Error: {e}")
        exit()
