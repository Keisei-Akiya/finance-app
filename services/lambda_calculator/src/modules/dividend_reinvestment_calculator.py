import polars as pl


def calculate_dividend_reinvestment(df_value: pl.DataFrame, df_dividend: pl.DataFrame) -> pl.DataFrame:
    try:
        df = (
            df_value
            # 価格と配当金データを結合
            .join(
                df_dividend,
                on=["investment_code", "date"],
                how="left",  # leftはdf_valueを基準に結合の意
            )
            .sort(["investment_code", "date"])
            .select(["investment_code", "date", "value_jpy", "dividend_jpy"])
        )

        unique_code = df["investment_code"].unique()

        # 配当金再投資を考慮したデータフレーム
        df_nav_list: list[pl.DataFrame] = []

        for code in unique_code:
            # 銘柄ごとのデータフレーム
            df_code: pl.DataFrame = df.filter(pl.col("investment_code") == code)
            initial_shares: float = 10000
            shares_list: list[float] = [initial_shares]

            for i in range(1, len(df_code)):
                # 前日の持ち株数
                prev_shares: float = shares_list[-1]

                # 当日の株価
                value: float = df_code["value_jpy"][i]

                # 当日の配当金
                # 配当金がない場合は前日の持ち株数をそのまま追加
                if df_code["dividend_jpy"][i] is None:
                    shares_list.append(prev_shares)
                    continue

                elif df_code["dividend_jpy"][i] > 0:
                    dividend: float = df_code["dividend_jpy"][i]
                    # 当日の配当金で購入できる株数
                    additional_shares: float = dividend * prev_shares // value
                    # 当日の持ち株数
                    shares_list.append(prev_shares + additional_shares)

            df_nav: pl.DataFrame = (
                df_code
                # 持ち株数
                .with_columns([pl.Series("shares", shares_list, dtype=pl.Float64)])
                # 基準価額
                .with_columns((pl.col("value_jpy") * pl.col("shares")).alias("nav_jpy"))
                # 絞る
                .select(["investment_code", "date", "nav_jpy"])
            )

            df_nav_list.append(df_nav)

        df_div_reinvest: pl.DataFrame = pl.concat(df_nav_list)

        return df_div_reinvest

    except Exception as e:
        print(f"Error: {e}")
        exit()
