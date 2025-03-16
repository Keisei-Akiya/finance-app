import streamlit as st

from Organisms.input import input


def backtesting() -> None:
    try:
        st.title("ポートフォリオのバックテスト")
        input()

        st.divider()

    except Exception as e:
        st.write(e)
