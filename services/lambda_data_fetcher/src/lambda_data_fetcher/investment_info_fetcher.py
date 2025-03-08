import os

import polars as pl
from dotenv import load_dotenv


def investment_info_fetcher() -> pl.DataFrame:
    try:
        # 環境変数を読み込む
        load_dotenv()

        # 環境変数からPostgreSQLの接続情報を取得
        DB_HOST: str | None = os.getenv("DB_HOST")
        DB_PORT: str | None = os.getenv("DB_PORT")
        DB_NAME: str | None = os.getenv("DB_NAME")
        DB_USER: str | None = os.getenv("DB_USER")
        DB_PASSWORD: str | None = os.getenv("DB_PASSWORD")

        # polars
        uri = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
        # query = "SELECT investment_code, ticker_symbol, country_code FROM public.investment_info"
        # TODO 開発用に20個ランダム抽出．実際は上を使う．
        query = "SELECT investment_code, ticker_symbol, country_code FROM public.investment_info ORDER BY random() LIMIT 20"
        df_investment_info: pl.DataFrame = pl.read_database_uri(query=query, uri=uri)

        return df_investment_info

    except Exception as e:
        print(f"投資コードとティッカーシンボルの取得に失敗しました: {e}")
        exit()

