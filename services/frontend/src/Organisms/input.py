import polars as pl
import streamlit as st

from Atoms.investment_info_fetcher import fetch_investment_info
from Molecules.add_ticker import add_ticker
from Molecules.check_sum_weight import check_sum_weight
from Organisms.analyse_button import analyse_button


def input() -> None:
    try:
        st.write("## ポートフォリオの設定")

        # 銘柄数の入力
        num_tickers: int = st.number_input("銘柄数 (20個まで)", 1, 20, 1)
        st.divider()

        # 投資銘柄マスタから銘柄情報を取得
        df_investment_info: pl.DataFrame = fetch_investment_info()

        # 銘柄の追加
        df: pl.DataFrame = add_ticker(num_tickers, df_investment_info)

        # ウェイトの合計値が100%かどうかをチェック
        check_sum_weight(df)

        # 分析ボタン
        analyse_button(df)

    except Exception as e:
        st.write(e)
