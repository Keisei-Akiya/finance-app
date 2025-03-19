import os

import httpx
import polars as pl
import streamlit as st
from dotenv import load_dotenv

from Organisms.output import output


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
        uri: str | None = os.getenv("LAMBDA_URI")
        if uri is None:
            st.write("環境変数 LAMBDA_URI が設定されていません")
            return False

        # polars dataframe to json
        json_data = df.to_dict(as_series=False)

        # Lambda に POST リクエストを送信
        r = httpx.post(uri, json=json_data)

        if r.status_code == 200:
            print("リクエストが成功しました")

            # 文字列型のbodyを渡す
            dict_result: dict = r.json()[0]
            body: str = dict_result["body"]
            output(body)

            return True

        else:
            st.write(f"リクエストが失敗しました: {r.status_code}")
            return False

    except Exception as e:
        st.write(e)
        return False
