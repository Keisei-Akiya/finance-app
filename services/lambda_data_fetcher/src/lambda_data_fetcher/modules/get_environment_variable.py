import os

from dotenv import load_dotenv


def get_environment_variable() -> dict[str, str | None]:
    try:
        load_dotenv()
        connection_config: dict[str, str | None] = {
            "dbname": os.getenv("DB_NAME"),
            "user": os.getenv("DB_USER"),
            "password": os.getenv("DB_PASSWORD"),
            "host": os.getenv("DB_HOST"),
            "port": os.getenv("DB_PORT"),
        }

        return connection_config

    except Exception as e:
        print(f"環境変数の取得に失敗しました: {e}")
        exit()
