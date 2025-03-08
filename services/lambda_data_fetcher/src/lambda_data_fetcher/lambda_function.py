import polars as pl
from dividend_data_formatter import dividend_data_formatter

# from dividend_data_saver import dividend_data_saver
from exchange_rate_fetcher import exchange_rate_fetcher
from historical_data_fetcher import historical_data_fetcher
from investment_info_fetcher import investment_info_fetcher
from value_data_formatter import value_data_formatter

# from value_data_saver import value_data_saver


def lambda_handler() -> None:
    try:
        # 為替レートを取得
        df_exchange_rate: pl.DataFrame = exchange_rate_fetcher()

        # 投資コードとティッカーシンボルを取得
        # investment_code_list: list[str]
        # ticker_symbol_list: list[str]
        # investment_code_list, ticker_symbol_list = investment_code_and_ticker_symbol_fetcher()
        df_investment_info: pl.DataFrame = investment_info_fetcher()

        # 投資銘柄のヒストリカルデータを取得
        historical_data: pl.DataFrame
        df_date: pl.DataFrame
        historical_data, df_date = historical_data_fetcher(df_investment_info=df_investment_info)

        # 価格履歴データを整える
        df_value: pl.DataFrame = value_data_formatter(
            historical_data=historical_data,
            df_date=df_date,
            df_exchange_rate=df_exchange_rate,
            investment_code_list=investment_code_list,
            ticker_symbol_list=ticker_symbol_list
        )
        print(df_value.head())

        # TODO 価格履歴データをPostgreSQLに保存
        # value_data_saver(df_value)

        # 配当データを整える
        df_dividend: pl.DataFrame = dividend_data_formatter(
            historical_data=historical_data,
            df_date=df_date,
            df_exchange_rate=df_exchange_rate,
            investment_code_list=investment_code_list,
            ticker_symbol_list=ticker_symbol_list
        )
        print(df_dividend.head())

        # TODO 配当データをPostgreSQLに保存
        # dividend_data_saver(df_dividend)
        return

    except Exception as e:
        print(f"失敗しました: {e}")
        exit()

if __name__ == "__main__":
    lambda_handler()
