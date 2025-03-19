import polars as pl

from modules.dividend_fetcher import dividend_fetcher
from modules.get_analysis_period import get_analysis_period
from modules.get_connection_config import get_connection_config
from modules.json_to_dataframe import json_to_dataframe
from modules.performance_calculator import calculate_performance
from modules.value_fetcher import value_fetcher


def lambda_handler(event: any = None, context: any = None) -> tuple[str, str]:
    try:
        # データベース接続情報を取得
        connection_config = get_connection_config()

        # TODO リクエストから銘柄コードとウェイトを取得
        df_code_and_weights: pl.DataFrame = json_to_dataframe(event)

        # 投資対象のデータを取得
        df_value: pl.DataFrame = value_fetcher(df_code_and_weights, connection_config)
        df_dividend: pl.DataFrame = dividend_fetcher(df_code_and_weights, connection_config)

        # 分析期間
        analysis_period: str = get_analysis_period(df_value)

        # 1年あたりの取引日数
        TRADING_DAYS_PER_YEAR = 252
        # パフォーマンス計算
        json_performance: str = calculate_performance(df_code_and_weights, df_value, df_dividend, TRADING_DAYS_PER_YEAR)
        print(json_performance)

        return analysis_period, json_performance

    except Exception as e:
        print(f"Error: {e}")
        exit()


if __name__ == "__main__":
    lambda_handler()
