import os

import psycopg2
import psycopg2._psycopg


def get_connection_config() -> psycopg2._psycopg.connection:
    try:
        # 環境変数からデータベース接続情報を取得
        try:
            config: dict[str, str | None] = {
                "host": os.getenv("DB_HOST"),
                "port": os.getenv("DB_PORT"),
                "dbname": os.getenv("DB_NAME"),
                "user": os.getenv("DB_USER"),
                "password": os.getenv("DB_PASSWORD"),
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
