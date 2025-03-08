import polars as pl


def dividend_data_duplicate_dropper(
    DB_HOST: str | None, DB_PORT: str | None, DB_USER: str | None, DB_PASSWORD: str | None, DB_NAME: str | None
) -> None:
    try:
        # polars
        uri = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
        query = "SELECT * FROM public.dividend_history"
        df_dividend: pl.DataFrame = pl.read_database_uri(query=query, uri=uri)

        # 重複数
        n_duplicate: int = len(df_dividend.filter(df_dividend.is_duplicated()))

        # 重複がある場合
        if n_duplicate != 0:
            df_dividend_drop_duplicate = df_dividend.unique(
                # この列だけを見れば一意に定まる．
                subset=["investment_code", "date"]
            )

            df_dividend_drop_duplicate.write_database(
                table_name="dividend_history",
                connection=f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}",
                if_table_exists="replace",
                engine="sqlalchemy",
            )
            print("配当データから重複を除きました。")

        else:
            print("配当データには重複はありませんでした。")

    except Exception as e:
        print(f"Error: {e}")
