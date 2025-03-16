import streamlit as st
from streamlit.delta_generator import DeltaGenerator


def label() -> None:
    try:
        grid: list[DeltaGenerator] = st.columns(4)

        with grid[0]:
            st.write("ティッカー")
        with grid[1]:
            st.write("ポートフォリオ1")
        with grid[2]:
            st.write("ポートフォリオ2")
        with grid[3]:
            st.write("ポートフォリオ3")

    except Exception as e:
        st.write(e)
