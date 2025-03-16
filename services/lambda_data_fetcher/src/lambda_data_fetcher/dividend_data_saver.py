import polars as pl
import psycopg2
import psycopg2._psycopg
from psycopg2.extras import execute_values


def dividend_data_saver(conn: psycopg2._psycopg.connection, df_dividend: pl.DataFrame) -> None:
    try:
        cur: psycopg2._psycopg.cursor = conn.cursor()

        # query
        insert_query: str = """
        INSERT INTO public.dividend_history (investment_code, date, dividend, dividend_jpy)
        VALUES %s
        ON CONFLICT (investment_code, date) DO NOTHING;
        """
        # for row in df_dividend.iter_rows(named=True):
        #     cur.execute(insert_query, (row["investment_code"], row["date"], row["dividend"], row["dividend_jpy"]))
        # conn.commit()

        records: list = [tuple(row) for row in df_dividend.to_numpy()]
        execute_values(cur, insert_query, records)
        conn.commit()

        print("配当データを保存しました。")

    except Exception as e:
        print(f"Error: {e}")

    finally:
        cur.close()
