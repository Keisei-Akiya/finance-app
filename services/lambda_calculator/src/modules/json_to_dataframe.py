import json
from io import StringIO

import polars as pl


def json_to_dataframe(event) -> pl.DataFrame:
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
    df_ticker_and_weights: pl.DataFrame = pl.DataFrame(event)

    return df_ticker_and_weights
