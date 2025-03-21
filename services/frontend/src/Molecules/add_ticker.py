import polars as pl
import streamlit as st

from Atoms.ticker_weight_form import ticker_weight_form


def add_ticker(num_tickers: int, df_investment_info: pl.DataFrame) -> pl.DataFrame:
    try:
        # ティッカーとウェイトを入力してDataFrameを作成
        all_ticker_weights: list[list[str | float]] = [
            ticker_weight_form(i, df_investment_info) for i in range(num_tickers)
        ]

        # 銘柄コードとウェイトのDataFrameを作成
        df: pl.DataFrame = (
            # まずティッカーとウェイトのDataFrameを作成
            pl.DataFrame(
                {
                    "ticker_and_name": [tw[0] for tw in all_ticker_weights],
                    "weight_pf1": [tw[1] for tw in all_ticker_weights],
                    "weight_pf2": [tw[2] for tw in all_ticker_weights],
                    "weight_pf3": [tw[3] for tw in all_ticker_weights],
                }
            )
            # 型指定
            .with_columns(
                pl.col("ticker_and_name").cast(pl.String),
                pl.col("weight_pf1").cast(pl.Float64),
                pl.col("weight_pf2").cast(pl.Float64),
                pl.col("weight_pf3").cast(pl.Float64),
            )
            # ticker_and_name で結合
            .join(df_investment_info, on="ticker_and_name", how="left")
            # カラムの整理
            .select(
                [
                    "investment_code",
                    "weight_pf1",
                    "weight_pf2",
                    "weight_pf3",
                ]
            )
        )

        return df

    except Exception as e:
        st.write(e)
        exit()
