import streamlit as st
from streamlit.delta_generator import DeltaGenerator

from Atoms.create_weight_input import create_weight_input


def ticker_weight_form(i: int) -> list[str | float]:
    try:
        # カラムを4つ作成
        grid: list[DeltaGenerator] = st.columns(4)

        # TODO ティッカーの選択肢を取得
        ticker_symbols: list[str] = ["VTI", "VGK", "VPL", "2511.T"]

        # 一番左のカラムにはティッカーのプルダウンを表示
        with grid[0]:
            st.selectbox(
                "ティッカー",
                options=ticker_symbols,
                index=None,
                key=f"ticker_symbol_{i}",
            )

        # 2番目以降のカラムで Weight (%)の入力
        for col in range(1, 4):
            create_weight_input(grid[col], f"weight_pf{col}_{i}")

        # list に格納
        ticker_weights: list[str | float] = [
            st.session_state[f"ticker_symbol_{i}"],
            st.session_state[f"weight_pf1_{i}"],
            st.session_state[f"weight_pf2_{i}"],
            st.session_state[f"weight_pf3_{i}"],
        ]

        # ウィジェットの値を返す
        return ticker_weights

    except Exception as e:
        st.write(e)
        exit()
