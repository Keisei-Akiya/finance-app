import streamlit as st
from streamlit.delta_generator import DeltaGenerator


def create_weight_input(grid: DeltaGenerator, key: str, i: int) -> None:
    """weightの入力欄

    Args:
        grid (DeltaGenerator): カラム番号
        key (str): キー
    """
    try:
        # ウェイトの更新を保持
        def update_weight() -> None:
            st.session_state[key] = st.session_state[key]

        # ウェイトの入力欄
        with grid:
            st.number_input(
                f"PF {i} ウェイト (%)",
                key=key,
                step=0.01,
                min_value=0.00,
                max_value=100.00,
                on_change=update_weight,
                help=f"ポートフォリオ {i} に占める重みを入力",
            )

    except Exception as e:
        st.write(e)
