import polars as pl


def value_data_saver(
    df_value: pl.DataFrame,
    DB_HOST: str | None,
    DB_PORT: str | None,
    DB_USER: str | None,
    DB_PASSWORD: str | None,
    DB_NAME: str | None,
) -> None:
    try:
        df_value.write_database(
            table_name="value_history",
            connection=f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}",
            if_table_exists="append",  # 重複データが生まれる可能性がある．
            engine="sqlalchemy",
        )
        print("価格データを保存しました。")

    except Exception as e:
        print(f"価格データの保存に失敗しました: {e}")
