import json
import os

import httpx
import polars as pl
import streamlit as st
from dotenv import load_dotenv


def send_to_lambda(df: pl.DataFrame) -> bool:
    """Lambdaにデータを送信する
    TODO: この関数を実装する

    Args:
        df (pd.DataFrame): _description_

    Returns:
        bool: _description_
    """

    try:
        load_dotenv()
        uri: str | None = os.getenv("API_GATEWAY_URI")
        if uri is None:
            st.write("環境変数 API_GATEWAY_URI が設定されていません")
            return False

        # polars dataframe to json
        json_data = df.to_dict(as_series=False)

        # Lambda に POST リクエストを送信
        r = httpx.post(uri, json=json_data)

        if r.status_code == 200:
            print("リクエストが成功しました")
            print(r.content)

            # 文字列型のbodyを渡す
            outer_json = json.loads(r.text)
            body_str = outer_json["body"]
            body = json.loads(body_str)
            print(body)

            analysis_period = body["analysis_period"]

            performance_str = body["performance"]
            performance = json.loads(performance_str)

            df_performance = pl.from_dicts(performance)

            st.write("## 分析結果")
            st.write(f"分析期間: {analysis_period}")
            st.write(df_performance)

            return True

        else:
            st.write(f"リクエストが失敗しました: {r.status_code}")
            return False

    except Exception as e:
        st.write(e)
        return False
