import pandas as pd
import requests
import streamlit as st


def send_to_lambda(df: pd.DataFrame) -> bool:
    try:
        # Pandas DataFrameをJSONに変換
        json_data = df.to_json(orient="records")
        st.write(json_data)

        # AWS Lambdaのエンドポイント
        # lambda_url: str = "https://xxxxxxxxxx.execute-api.ap-northeast-1.amazonaws.com/default/lambda_function"

        # response = requests.post(lambda_url, json=json_data)

        # if response.status_code == 200:
        #     st.write("正常に送信されました")
        #     return True
        # else:
        #     st.write(f"リクエストが失敗しました: {response.status_code}")
        #     return False

    except Exception as e:
        st.write(e)
        return False
