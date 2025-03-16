import json

import polars as pl


def json_to_dataframe() -> pl.DataFrame:
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
    # TODO 仮の JSON データ
    df_ticker_and_weights: pl.DataFrame = pl.read_json("./test.json")

    return df_ticker_and_weights
