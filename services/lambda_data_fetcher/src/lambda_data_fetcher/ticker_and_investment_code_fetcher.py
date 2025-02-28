import os

import psycopg2
from dotenv import load_dotenv


def ticker_and_investment_code_fetcher() -> tuple[list[str], list[str]]:
    try:
        # 環境変数を読み込む
        env_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), ".env")
        load_dotenv(dotenv_path=env_path)

        # 環境変数からPostgreSQLの接続情報を取得
        DB_HOST: str | None = os.getenv("DB_HOST")
        DB_PORT: str | None = os.getenv("DB_PORT")
        DB_NAME: str | None = os.getenv("DB_NAME")
        DB_USER: str | None = os.getenv("DB_USER")
        DB_PASSWORD: str | None = os.getenv("DB_PASSWORD")

        # PostgreSQLに接続
        conn: psycopg2.connection = psycopg2.connect(
            host=DB_HOST,
            port=DB_PORT,
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD
        )
        print("PostgreSQLへの接続に成功しました")

        # TODO ティッカーシンボルと `investment_code` を取得
        # 仮置き
        ticker_list: list[str] = ["VOO", "VGK", "VPL", "VWO"]
        investment_code_list: list[str] = ["askdf", "rytajvkhal", "danfhaio", "adslfuo"]

        return ticker_list, investment_code_list

    except Exception as e:
        print(f"ティッカーシンボルと投資コードの取得に失敗しました: {e}")
        exit()

    finally:
        # PostgreSQLとの接続を切断
        conn.close()