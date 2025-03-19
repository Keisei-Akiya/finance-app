import numpy as np
import polars as pl

from modules.calculate_covariance_matrix import calculate_covariance_matrix
from modules.calculate_sigma_pf import calculate_sigma_pf


def calculate_volatility(
    df_code_and_weights: pl.DataFrame, df_value: pl.DataFrame, TRADING_DAYS_PER_YEAR: int
) -> np.ndarray:
    try:
        # 共分散行列を計算
        cov_matrix: np.ndarray = calculate_covariance_matrix(df_value)

        # ポートフォリオの数
        num_pf: int = 3

        # ポートフォリオのボラティリティを計算
        volatility_list: list[np.float64] = [
            calculate_sigma_pf(df_code_and_weights, cov_matrix, str(i + 1), TRADING_DAYS_PER_YEAR)
            for i in range(num_pf)
        ]

        # リストをnumpy配列に変換
        volatility_array: np.ndarray = np.array(volatility_list)

        return volatility_array

    except Exception as e:
        print(f"ボラティリティの計算に失敗しました: {e}")
        exit()
