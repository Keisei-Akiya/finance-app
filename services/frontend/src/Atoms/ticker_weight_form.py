import polars as pl
import streamlit as st
from streamlit.delta_generator import DeltaGenerator

from Atoms.create_weight_input import create_weight_input


def ticker_weight_form(i: int, df_investment_info: pl.DataFrame) -> list[str | float]:
    try:
        # 投資銘柄マスタからティッカーシンボルを取得
        ticker_options: list[str] = df_investment_info["ticker_and_name"].to_list()

        # 一番左のカラムにはティッカーのプルダウンを表示
        st.selectbox(
            "銘柄",
            options=ticker_options,
            index=None,
            key=f"ticker_and_name_{i}",
            help="日本の銘柄は英数字が全角になっている場合があります．",
        )

        # カラムを4つ作成
        grid: list[DeltaGenerator] = st.columns(4)

        # 2番目以降のカラムで Weight (%)の入力
        for col in range(1, 4):
            create_weight_input(grid[col], f"weight_pf{col}_{i}", i=col)

        # list に格納
        ticker_weights: list[str | float] = [
            st.session_state[f"ticker_and_name_{i}"],
            st.session_state[f"weight_pf1_{i}"],
            st.session_state[f"weight_pf2_{i}"],
            st.session_state[f"weight_pf3_{i}"],
        ]

        # ウィジェットの値を返す
        return ticker_weights

    except Exception as e:
        st.write(e)
        exit()
