import polars as pl
import psycopg2
import psycopg2._psycopg
from psycopg2.extras import execute_values


def value_data_saver(conn: psycopg2._psycopg.connection, df_value: pl.DataFrame) -> None:
    try:
        # カーソルを取得
        cur: psycopg2._psycopg.cursor = conn.cursor()

        # query 重複データは挿入しない
        insert_query: str = """
        INSERT INTO public.value_history (investment_code, date, value, value_jpy)
        VALUES %s
        ON CONFLICT (investment_code, date) DO NOTHING;
        """

        # for row in df_value.iter_rows(named=True):
        #     cur.execute(insert_query, (row["investment_code"], row["date"], row["value"], row["value_jpy"]))
        # conn.commit()

        records: list = [tuple(row) for row in df_value.to_numpy()]
        execute_values(cur, insert_query, records)
        conn.commit()

        print("価格データを保存しました。")

    except Exception as e:
        print(f"価格データの保存に失敗しました: {e}")

    finally:
        cur.close()
