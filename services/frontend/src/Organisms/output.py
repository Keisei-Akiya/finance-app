import json

import polars as pl
import streamlit as st


def output(body: str) -> None:
    try:
        st.write("## 分析結果")

        # TODO 分析期間

        # ポートフォリオのリターン、ボラティリティ、シャープレシオを受け取る
        # strを辞書型に変換
        body_json: dict = json.loads(body)

        # データフレームに変換
        df_result: pl.DataFrame = pl.DataFrame(body_json)

        # 結果を表示
        st.write(df_result)

    except Exception as e:
        st.write(e)
