import os

import psycopg2
import psycopg2._psycopg


def get_connection_config() -> psycopg2._psycopg.connection:
    try:
        # 環境変数からデータベース接続情報を取得
        try:
            config: dict[str, str] = {
                "DB_HOST": os.environ["DB_HOST"],
                "DB_PORT": os.environ["DB_PORT"],
                "DB_NAME": os.environ["DB_NAME"],
                "DB_USER": os.environ["DB_USER"],
                "DB_PASS": os.environ["DB_PASSWORD"],
            }

        except KeyError as e:
            print(f"Error: {e}")
            return {"error": str(e)}

        # データベースに接続
        try:
            conn = psycopg2.connect(**config)
            return conn

        except Exception as e:
            print(f"Error: {e}")
            return {"error": str}

    except Exception as e:
        print(f"Error: {e}")
        return {"error": str(e)}
