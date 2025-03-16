import numpy as np
import polars as pl


def calculate_covariance_matrix(df_value: pl.DataFrame) -> np.ndarray:
    try:
        # pivot table に変換
        df_value_pivot: pl.DataFrame = (
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
            .drop("date")
            # 欠損のある行を削除
            .drop_nulls()
        )

        # 日次対数階差に変換
        df_log_return: pl.DataFrame = (
            df_value_pivot
            # すべてのカラムに対して対数階差を計算
            .select([pl.all().log().diff()])
            # 先頭行のnullを削除
            .drop_nulls()
        )

        # 共分散行列を計算
        cov_matrix: np.ndarray = np.cov(
            df_log_return.to_numpy(),
            # rowは日付を表し，varではないため．
            rowvar=False,
        )

        return cov_matrix

    except Exception as e:
        print(f"共分散行列の計算に失敗しました: {e}")
        exit()
