import httpx
import pandas as pd
import streamlit as st


def send_to_lambda(df: pd.DataFrame) -> bool:
    """Lambdaにデータを送信する
    TODO: この関数を実装する

    Args:
        df (pd.DataFrame): _description_

    Returns:
        bool: _description_
    """
    try:
        # Pandas DataFrameをJSONに変換
        json_data = df.to_json(orient="records")
        st.write(json_data)

        # AWS Lambdaのエンドポイント
        lambda_url: str = "https://xxxxxxxxxx.execute-api.ap-northeast-1.amazonaws.com/default/lambda_function"

        r = httpx.post(lambda_url, json=json_data)

        if r.status_code == 200:
            st.write("正常に送信されました")
            return True
        else:
            st.write(f"リクエストが失敗しました: {r.status_code}")
            return False

    except Exception as e:
        st.write(e)
        return False
