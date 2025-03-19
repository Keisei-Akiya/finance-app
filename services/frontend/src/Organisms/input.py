import pandas as pd
import streamlit as st

from Atoms.label import label
from Molecules.add_ticker import add_ticker
from Molecules.check_sum_weight import check_sum_weight
from Organisms.analyse_button import analyse_button


def input() -> None:
    try:
        st.write("## ポートフォリオの設定")

        # 銘柄数の入力
        num_tickers: int = st.number_input("銘柄数 (20個まで)", 1, 20, 1)
        st.divider()

        # ラベル．(PF1，PF2，PF3)
        label()

        # 銘柄の追加
        df: pd.DataFrame = add_ticker(num_tickers)

        # ウェイトの合計値が100%かどうかをチェック
        check_sum_weight(df)

        # 分析ボタン
        analyse_button(df)

    except Exception as e:
        st.write(e)
