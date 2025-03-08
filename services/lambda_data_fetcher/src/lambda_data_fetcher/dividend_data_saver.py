import polars as pl


def dividend_data_saver(
    df_dividend: pl.DataFrame,
    DB_HOST: str | None,
    DB_PORT: str | None,
    DB_USER: str | None,
    DB_PASSWORD: str | None,
    DB_NAME: str | None,
) -> None:
    try:
        df_dividend.write_database(
            table_name="dividend_history",
            connection=f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}",
            if_table_exists="append",  # 重複データが生まれる可能性がある．
            engine="sqlalchemy",
        )
        print("配当データを保存しました。")

    except Exception as e:
        print(f"Error: {e}")
