import pandas as pd
import streamlit as st


def calc_sum_and_select_color(df: pd.DataFrame, column_name: str) -> None:
    sum_weight: float = df[column_name].sum()

    # 0%の場合は色指定しない
    if sum_weight == 0:
        st.write(f"{sum_weight:.2f}%")

    # 100%の場合は緑色
    elif sum_weight == 100:
        st.write(f":green[{sum_weight:.0f}]%")

    # それ以外は赤色
    else:
        st.write(f":red[{sum_weight:.2f}]%")
