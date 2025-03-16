import numpy as np
import polars as pl
from dividend_reinvestment_calculator import calculate_dividend_reinvestment


def calculate_cagr(
    df_code_and_weights: pl.DataFrame, df_value: pl.DataFrame, df_dividend: pl.DataFrame, TRADING_DAYS_PER_YEAR: int
) -> np.ndarray:
    try:
        # 投資対象のコードを取得
        # print(df_code_and_weights)
        unique_code: pl.Series = df_code_and_weights["investment_code"].unique()

        # 配当金再投資の価格推移を計算
        df_div_reinvest: pl.DataFrame = calculate_dividend_reinvestment(df_value, df_dividend)
        # print(df_div_reinvest)

        # リターン (CAGR) を計算
        cagr_dict: dict[str, np.float64] = {}
        for code in unique_code:
            # 銘柄ごとのデータフレーム
            df_code: pl.DataFrame = df_div_reinvest.filter(pl.col("investment_code") == code).sort("date")

            # 最後と最初の値を出力
            v_last: np.float64 = df_code["nav_jpy"].to_numpy()[-1]
            v_first: np.float64 = df_code["nav_jpy"].to_numpy()[0]

            n_years: float = len(df_code) / TRADING_DAYS_PER_YEAR
            cagr: np.float64 = (v_last / v_first) ** (1 / n_years) - 1

            # 辞書に追加
            cagr_dict[code] = cagr

        df_cagr: pl.DataFrame = pl.DataFrame({"investment_code": cagr_dict.keys(), "cagr": cagr_dict.values()})

        df = df_code_and_weights.join(df_cagr, on="investment_code", how="left")

        num_pf: int = 3
        cagr_list: list[np.float64] = [
            df[f"weight_pf{i + 1}"].to_numpy() @ df["cagr"].to_numpy() for i in range(num_pf)
        ]

        cagr_array: np.ndarray = np.array(cagr_list)

        return cagr_array

    except Exception as e:
        print(f"Error: {e}")
        exit()
