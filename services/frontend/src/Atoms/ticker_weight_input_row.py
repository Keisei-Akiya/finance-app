import streamlit as st
from streamlit.delta_generator import DeltaGenerator


def ticker_weight_input_row(i: int) -> tuple[str | None, float, float, float]:
    try:
        grid: list[DeltaGenerator] = st.columns(4)

        with grid[0]:
            st.selectbox(
                "Ticker",
                ("AAPL", "GOOGL", "AMZN", "MSFT", "TSLA"),
                index=None,
                key=f"ticker_symbol_{i}",
            )

        # Weight (%)の入力

        # pf1
        # ウィジェットの値が変更されたときに呼び出される関数
        def update_pf1_weight() -> None:
            st.session_state[f"weight_pf1_{i}"] = st.session_state[f"weight_pf1_{i}"]

        # ウィジェットの作成
        with grid[1]:
            st.number_input(
                "Weight (%)",
                key=f"weight_pf1_{i}",
                step=0.01,
                min_value=0.00,
                max_value=100.00,
                on_change=update_pf1_weight,
            )

        # pf2
        # ウィジェットの値が変更されたときに呼び出される関数
        def update_pf2_weight() -> None:
            st.session_state[f"weight_pf2_{i}"] = st.session_state[f"weight_pf2_{i}"]

        # ウィジェットの作成
        with grid[2]:
            st.number_input(
                "Weight (%)",
                key=f"weight_pf2_{i}",
                step=0.01,
                min_value=0.00,
                max_value=100.00,
                on_change=update_pf2_weight,
            )

        # pf3
        # ウィジェットの値が変更されたときに呼び出される関数
        def update_pf3_weight() -> None:
            st.session_state[f"weight_pf3_{i}"] = st.session_state[f"weight_pf3_{i}"]

        # ウィジェットの作成
        with grid[3]:
            st.number_input(
                "Weight (%)",
                key=f"weight_pf3_{i}",
                step=0.01,
                min_value=0.00,
                max_value=100.00,
                on_change=update_pf3_weight,
            )

        # ウィジェットの値を返す
        return (
            st.session_state[f"ticker_symbol_{i}"],
            st.session_state[f"weight_pf1_{i}"],
            st.session_state[f"weight_pf2_{i}"],
            st.session_state[f"weight_pf3_{i}"],
        )

    except Exception as e:
        st.write(e)
        return None, 0.0, 0.0, 0.0
