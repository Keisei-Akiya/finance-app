import pandas as pd
import streamlit as st

from Atoms.ticker_weight_form import ticker_weight_form


def add_ticker(num_tickers: int) -> pd.DataFrame:
    try:
        # 選択式のプルダウンでティッカーを選択
        all_ticker_weights: list[list[str | float]] = [ticker_weight_form(i) for i in range(num_tickers)]

        # ティッカー，PF1，PF2，PF3のリストを返す
        df: pd.DataFrame = pd.DataFrame(
            all_ticker_weights,
            columns=["ticker_symbol", "weight_pf1", "weight_pf2", "weight_pf3"],
        )

        return df

    except Exception as e:
        st.write(e)
