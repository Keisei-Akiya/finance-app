import polars as pl


def dividends_reinvestment_return(data: pl.DataFrame, initial_shares: int) -> pl.DataFrame:
    """
    配当金再投資をシミュレーションする関数
    :param data: 終値と配当金があるデータフレーム
    :param initial_shares: 初日の持ち株数
    :return: 配当金再投資を考慮したデータフレーム
    """
    shares_list: list[int] = [initial_shares]

    for i in range(1, len(data)):
        # 前日の持ち株数
        prev_shares = shares_list[-1]

        # 当日の配当金
        dividend = data["Dividends"][i]

        # 当日の株価
        price = data["Close"][i]

        # 当日の配当金で購入できる株数
        additional_shares = dividend * prev_shares // price

        # 当日の持ち株数
        shares_list.append(prev_shares + additional_shares)

    data = (
        data
        # 持ち株数
        .with_columns([pl.Series("Shares", shares_list, dtype=pl.Float64)])
        # 持ち株の時価総額
        .with_columns((pl.col("Close") * pl.col("Shares")).alias("Value"))
        # 時価総額の対数
        .with_columns((pl.col("Value").log()).alias("LogValue"))
    )

    data: pl.DataFrame = (
        data
        # 対数累積リターン
        .with_columns((pl.col("LogValue") - data["LogValue"][0]).alias("LogReturn"))
        # 累積リターン
        .with_columns(((pl.col("LogReturn").exp() - 1) * 100).alias("Return"))
    )

    return data
