import polars as pl
import streamlit as st


def validate_weights(df: pl.DataFrame) -> bool:
    """入力されたウェイトのバリデーションを行う

    Args:
        df (pd.DataFrame): 入力されたウェイトのデータフレーム


    """
    try:
        pf1 = df["weight_pf1"].sum()
        pf2 = df["weight_pf2"].sum()
        pf3 = df["weight_pf3"].sum()

        # PF1 100
        if pf1 == 100 and pf2 == 0 and pf3 == 0:
            return True

        # PF1とPF2 100
        elif pf1 == 100 and pf2 == 100 and pf3 == 0:
            return True

        # 全部 100
        elif pf1 == 100 and pf2 == 100 and pf3 == 100:
            return True

        else:
            st.write("ウェイトの合計値が100%になっていません")
            return False

    except Exception as e:
        st.write(e)
        return False
