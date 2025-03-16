import pandas as pd
import streamlit as st

from Atoms.label import label
from Molecules.add_ticker import add_ticker
from Molecules.check_sum_weight import check_sum_weight
from Organisms.analyse_button import analyse_button


def input() -> None:
    try:
        st.write("## ポートフォリオの設定")
        num_tickers: int = st.number_input("銘柄数 (10個まで)", 1, 10, 1)
        # num_tickers: int = 10

        # ラベル．(ティッカー，PF1，PF2，PF3)
        label()
        # ティッカーの追加
        df: pd.DataFrame = add_ticker(num_tickers)

        # TODO 合計
        check_sum_weight(df)

        analyse_button(df)

    except Exception as e:
        st.write(e)
