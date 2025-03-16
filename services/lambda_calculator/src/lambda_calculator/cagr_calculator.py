import numpy as np
import polars as pl

# from dividend_reinvestment_calculator import calculate_dividend_reinvestment


def calculate_cagr(
    df_code_and_weights: pl.DataFrame, df_value: pl.DataFrame, df_dividend: pl.DataFrame, TRADING_DAYS_PER_YEAR: int
) -> np.ndarray:
    try:
        # 投資対象の数
        # num_investment: int = len(df_code_and_weights)

        # 配当金再投資の価格推移を計算
        # df_div_reinvest: pl.DataFrame = calculate_dividend_reinvestment(df_value, df_dividend)

        # リターン (CAGR) を計算
        cagr_array: np.ndarray = np.array([0.5, 0.6, 0.7])

        return cagr_array

    except Exception as e:
        print(f"Error: {e}")
        exit()
