import polars as pl
import streamlit as st
from streamlit.delta_generator import DeltaGenerator

from Atoms.calc_sum_and_select_color import calc_sum_and_select_color


def check_sum_weight(df: pl.DataFrame) -> None:
    try:
        grid: list[DeltaGenerator] = st.columns(4)

        with grid[0]:
            st.write("合計")

        with grid[1]:
            calc_sum_and_select_color(df, "weight_pf1")

        with grid[2]:
            calc_sum_and_select_color(df, "weight_pf2")

        with grid[3]:
            calc_sum_and_select_color(df, "weight_pf3")

    except Exception as e:
        st.write(e)
