import polars as pl


def json_to_dataframe(event: any = None) -> pl.DataFrame:
    """
    Convert JSON data to a Polars DataFrame.

    Parameters
    ----------
    json_data : str
        JSON data.

    Returns
    -------
    pl.DataFrame
        Polars DataFrame.
    """

    # JSONをDataFrameに変換
    # df_code_and_weights: pl.DataFrame = pl.DataFrame(event)

    # 仮
    df_code_and_weights: pl.DataFrame = pl.read_json("./test.json")

    return df_code_and_weights
