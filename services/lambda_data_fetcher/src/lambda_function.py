import polars as pl
import psycopg2
import psycopg2._psycopg
from modules.dividend_data_formatter import dividend_data_formatter
from modules.dividend_data_saver import dividend_data_saver
from modules.exchange_rate_fetcher import exchange_rate_fetcher
from modules.get_environment_variable import get_environment_variable
from modules.historical_data_fetcher import historical_data_fetcher
from modules.investment_info_fetcher import investment_info_fetcher
from modules.value_data_formatter import value_data_formatter
from modules.value_data_saver import value_data_saver


def lambda_handler(event, context) -> None:
    try:
        # PostgreSQLへの接続情報
        connection_config: dict[str, str | None] = get_environment_variable()

        # データベースへの接続
        conn: psycopg2._psycopg.connection = psycopg2.connect(**connection_config)

        # 為替レートを取得
        # 日次
        df_exchange_rate: pl.DataFrame = exchange_rate_fetcher()

        # 投資コードとティッカーシンボルを取得
        df_investment_info: pl.DataFrame = investment_info_fetcher(conn)

        # 投資銘柄のヒストリカルデータを取得
        df_value_pivot: pl.DataFrame
        df_dividend_pivot: pl.DataFrame
        df_value_pivot, df_dividend_pivot = historical_data_fetcher(df_investment_info)

        # データの整形
        df_value: pl.DataFrame = value_data_formatter(df_value_pivot, df_exchange_rate, df_investment_info)
        df_dividend: pl.DataFrame = dividend_data_formatter(df_dividend_pivot, df_exchange_rate, df_investment_info)

        # 保存
        value_data_saver(conn, df_value)
        dividend_data_saver(conn, df_dividend)

    except Exception as e:
        print(f"失敗しました: {e}")
        exit()

    finally:
        # データベースへの接続を切断
        conn.close()


if __name__ == "__main__":
    lambda_handler(event, context)
