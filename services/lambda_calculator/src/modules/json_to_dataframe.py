import polars as pl


def json_to_dataframe(event: dict) -> pl.DataFrame:
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
    try:
        # JSONをDataFrameに変換
        df_code_and_weights: pl.DataFrame = pl.DataFrame(event)

        if len(df_code_and_weights) == 0:
            df_code_and_weights = pl.read_json("./test.json")

        return df_code_and_weights

    except Exception as e:
        print(f"Error: {e}")
        exit()
