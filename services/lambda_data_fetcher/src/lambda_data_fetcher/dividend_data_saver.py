import polars as pl
import psycopg2


def dividend_data_saver(data: pl.DataFrame) -> None:
    try:

    except Exception as e:
        print(f"Error: {e}")
        raise e
    finally:
        conn.close()
        cur.close()