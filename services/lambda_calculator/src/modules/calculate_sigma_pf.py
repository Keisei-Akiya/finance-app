import numpy as np
import polars as pl


def calculate_sigma_pf(
    df_code_and_weights: pl.DataFrame, cov_matrix: np.ndarray, pf_num: str, TRADING_DAYS_PER_YEAR: int
) -> np.float64:
    try:
        # 重みを取得
        weights: np.ndarray = df_code_and_weights[f"weight_pf{pf_num}"].to_numpy()
        # 1年の取引日数
        # ポートフォリオの分散
        sigma2_pf: np.float64 = weights @ cov_matrix @ weights
        # ポートフォリオの年率ボラティリティ
        sigma_pf: np.float64 = np.sqrt(sigma2_pf) * np.sqrt(TRADING_DAYS_PER_YEAR)

        return sigma_pf

    except Exception as e:
        print(f"ポートフォリオ{pf_num}のボラティリティの計算に失敫しました: {e}")
        exit()
