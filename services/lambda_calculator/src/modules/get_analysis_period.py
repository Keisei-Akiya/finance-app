import polars as pl


def get_analysis_period(df_value: pl.DataFrame) -> str:
    """
    Get the analysis period.

    Parameters
    ----------
    df_code_and_weights : pl.DataFrame
        DataFrame containing the stock codes and weights.
    df_value : pl.DataFrame
        DataFrame containing the stock prices.

    Returns
    -------
    int
        Analysis period.
    """
    try:
        # 分析期間

        # pivot table に変換
        df: pl.DataFrame = (
            df_value
            # 重みと順番を合わせるためにinvestment_codeでソート
            .sort("investment_code")
            # investment_codeをカラム名としたピボットテーブルに変換
            .pivot(
                "investment_code",
                index="date",
                values=["value_jpy"],
            )
            # 時間軸でソート
            .sort("date")
            # dateカラムを削除
            # 欠損のある行を削除
            .drop_nulls()
        )

        start_date = df["date"].min()
        end_date = df["date"].max()

        analysis_period: str = f"{start_date} ~ {end_date}"

        return analysis_period

    except Exception as e:
        print(f"Error: {e}")
        exit()
