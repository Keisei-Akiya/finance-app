import numpy as np
import polars as pl


def calculate_dividend_reinvestment(df_value: pl.DataFrame, df_dividend: pl.DataFrame) -> pl.DataFrame:
    try:
        df = (
            df_value
            # 配当金を結合
            .join(
                df_dividend,
                on=["investment_code", "date"],
                # leftはdf_valueを基準に結合の意
                how="left",
            )
            # ソート
            .sort(["investment_code", "date"])
            .select(["investment_code", "date", "value_jpy", "dividend_jpy"])
        )
        print(df.head())

        unique_code = df["investment_code"].unique()
        print(unique_code)

        df_div_reinvest: pl.DataFrame = pl.DataFrame()
        return df_div_reinvest

    except Exception as e:
        print(f"Error: {e}")
        exit()
