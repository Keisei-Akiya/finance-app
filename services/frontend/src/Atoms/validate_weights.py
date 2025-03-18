import pandas as pd
import streamlit as st


def validate_weights(df: pd.DataFrame) -> bool:
    """入力されたウェイトのバリデーションを行う

    Args:
        df (pd.DataFrame): _description_


    """
    try:
        # PF1
        # 100以外は入力できない
        if not df["weight_pf1"].sum() == 100:
            st.write("ポートフォリオ1のウェイトの合計が100%になるようにしてください")
            return False

        # PF2
        elif df["weight_pf2"].sum() == 0:
            return True

        elif not df["weight_pf2"].sum() == 100:
            st.write("ポートフォリオ2のウェイトの合計は0か100%になるようにしてください")
            return False

        # PF3
        elif df["weight_pf3"].sum() == 0:
            return True

        elif not df["weight_pf3"].sum() == 100:
            st.write("ポートフォリオ3のウェイトの合計は0か100%になるようにしてください")
            return False

        return True

    except Exception as e:
        st.write(e)
        return False
