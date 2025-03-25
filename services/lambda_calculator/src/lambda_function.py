import json

import polars as pl
import psycopg2
import psycopg2._psycopg
from aws_lambda_typing import context as lambda_context

from modules.dividend_fetcher import dividend_fetcher
from modules.get_analysis_period import get_analysis_period
from modules.get_connection_config import get_connection_config
from modules.json_to_dataframe import json_to_dataframe
from modules.performance_calculator import calculate_performance
from modules.value_fetcher import value_fetcher


def lambda_handler(event: dict = None, context: lambda_context = None) -> tuple[str, str]:
    try:
        # データベース接続情報を取得
        conn: psycopg2._psycopg.connection = get_connection_config()

        # TODO リクエストから銘柄コードとウェイトを取得
        df_code_and_weights: pl.DataFrame = json_to_dataframe(event)

        # 投資対象のデータを取得
        df_value: pl.DataFrame = value_fetcher(df_code_and_weights, conn)
        df_dividend: pl.DataFrame = dividend_fetcher(df_code_and_weights, conn)

        # 分析期間
        analysis_period: str = get_analysis_period(df_value)

        # 1年あたりの取引日数
        TRADING_DAYS_PER_YEAR: int = 252
        # パフォーマンス計算
        json_performance: dict[str, str | float] = calculate_performance(
            df_code_and_weights, df_value, df_dividend, TRADING_DAYS_PER_YEAR
        )
        print(json_performance)

        response_body = {"analysis_period": analysis_period, "performance": json_performance}

        return {"statusCode": 200, "body": json.dumps(response_body), "headers": {"Content-Type": "application/json"}}

    except Exception as e:
        print(f"Error: {e}")
        exit()

    finally:
        # データベース接続をクローズ
        conn.close()


if __name__ == "__main__":
    lambda_handler()
