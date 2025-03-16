import pandas as pd
import streamlit as st

from Atoms.ticker_weight_input_row import ticker_weight_input_row


def add_ticker(num_tickers: int) -> pd.DataFrame:
    try:
        # 選択式のプルダウンでティッカーを選択
        ticker_symbol_list: list[str | None] = []
        weight_list_pf1: list[float] = []
        weight_list_pf2: list[float] = []
        weight_list_pf3: list[float] = []

        i: int
        for i in range(num_tickers):
            ticker_symbol, weight_pf1, weight_pf2, weight_pf3 = ticker_weight_input_row(i)

            # ウィジェットの値をリストに追加
            ticker_symbol_list.append(ticker_symbol)
            weight_list_pf1.append(weight_pf1)
            weight_list_pf2.append(weight_pf2)
            weight_list_pf3.append(weight_pf3)

        # ティッカー，PF1，PF2，PF3のリストを返す
        df: pd.DataFrame = pd.DataFrame(
            {
                "ticker_symbol": ticker_symbol_list,
                "weight_pf1": weight_list_pf1,
                "weight_pf2": weight_list_pf2,
                "weight_pf3": weight_list_pf3,
            }
        )
        return df

    except Exception as e:
        st.write(e)
