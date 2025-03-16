# import polars as pl
import pandas as pd
import streamlit as st


def output() -> None:
    try:
        st.write("## 分析結果")

        # TODO 分析期間

        # TODO ポートフォリオのリターン、ボラティリティ、シャープレシオを受け取る

        # 借り置き
        pf_1_return: float = 0.07
        pf_1_volatility: float = 0.15
        pf_1_sharpe_ratio: float = pf_1_return / pf_1_volatility

        pf_2_return: float = 0.08
        pf_2_volatility: float = 0.14
        pf_2_sharpe_ratio: float = pf_2_return / pf_2_volatility

        pf_3_return: float = 0.09
        pf_3_volatility: float = 0.13
        pf_3_sharpe_ratio: float = pf_3_return / pf_3_volatility

        # テーブル表示
        df: pd.DataFrame = pd.DataFrame(
            {
                "": ["リターン", "ボラティリティ", "シャープレシオ"],
                "PF 1": [pf_1_return, pf_1_volatility, pf_1_sharpe_ratio],
                "PF 2": [pf_2_return, pf_2_volatility, pf_2_sharpe_ratio],
                "PF 3": [pf_3_return, pf_3_volatility, pf_3_sharpe_ratio],
            }
        )
        st.table(df)

    except Exception as e:
        st.write(e)
