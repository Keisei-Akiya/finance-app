import polars as pl
import streamlit as st

from Atoms.validate_ticker_symbols import validate_ticker_symbols
from Atoms.validate_weights import validate_weights
from Organisms.output import output
from Organisms.send_to_lambda import send_to_lambda


def analyse_button(df: pl.DataFrame) -> None:
    try:
        if st.button("分析開始"):
            # 正常に動作した場合リクエストを送信
            if validate_ticker_symbols(df) and validate_weights(df):
                # データを送信できた場合
                if send_to_lambda(df):
                    # データを受け取った場合
                    output()

    except Exception as e:
        st.write(e)
