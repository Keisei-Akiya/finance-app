import polars as pl
import streamlit as st


def validate_ticker_symbols(df: pl.DataFrame) -> bool:
    """入力されたティッカーシンボルのバリデーションを行う

    Args:
        df (pd.DataFrame): _description_


    """
    try:
        # エラーメッセージ
        if df["investment_code"].is_null().sum() > 0:
            st.write("ティッカーシンボルを入力してください")
            return False

        elif df["investment_code"].is_duplicated().any():
            st.write("ティッカーシンボルが重複しています")
            return False

        return True

    except Exception as e:
        st.write(e)
        return False
