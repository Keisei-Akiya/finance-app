import pandas as pd
import streamlit as st


def validate_weights(df: pd.DataFrame) -> bool:
    """入力されたウェイトのバリデーションを行う

    Args:
        df (pd.DataFrame): _description_


    """
    try:
        # PF1のウェイトは必ず入力
        if 0 <= df["weight_pf1"].sum() < 100:
            st.write("ポートフォリオ1のウェイトの合計が100%になるようにしてください")
            return False

        # PF2のウェイトは0でも良い
        elif 0 < df["weight_pf2"].sum() < 100:
            st.write("ポートフォリオ2のウェイトの合計が100%になるようにしてください")
            return False

        # PF3のウェイトは0でも良い
        elif 0 < df["weight_pf3"].sum() < 100:
            st.write("ポートフォリオ3のウェイトの合計が100%になるようにしてください")
            return False

        return True

    except Exception as e:
        st.write(e)
        return False
