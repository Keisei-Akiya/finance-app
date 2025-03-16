import os

from dotenv import load_dotenv


def get_connection_config() -> dict:
    try:
        load_dotenv()
        connection_config: dict = {
            "host": os.getenv("DB_HOST"),
            "port": os.getenv("DB_PORT"),
            "user": os.getenv("DB_USER"),
            "password": os.getenv("DB_PASSWORD"),
            "dbname": os.getenv("DB_NAME"),
        }
        return connection_config

    except Exception as e:
        print(f"Error: {e}")
        return {"error": str(e)}
