import pandas as pd
import streamlit as st


def validate_ticker_symbols(df: pd.DataFrame) -> bool:
    """入力されたティッカーシンボルのバリデーションを行う

    Args:
        df (pd.DataFrame): _description_


    """
    try:
        # エラーメッセージ
        if df["ticker_symbol"].isnull().sum() > 0:
            st.write("ティッカーシンボルを入力してください")
            return False

        elif df["ticker_symbol"].duplicated().sum() > 0:
            st.write("ティッカーシンボルが重複しています")
            return False

        return True

    except Exception as e:
        st.write(e)
        return False
