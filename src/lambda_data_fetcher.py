# ライブラリのインポート
import polars as pl
import yfinance as yf

# ティッカーシンボルのリスト
tickers = ["VOO", "VGK", "JPY=X"]

# yFinance を使って株価データを取得
yf_tickers = yf.Tickers(tickers=tickers)
historical_data = yf_tickers.history(period="max")

# 終値をpolarsのDataFrameに変換
df_close = pl.DataFrame(historical_data["Close"])

# 円換算の終値を追加
expr_list = [
    # 終値に為替レートを掛け算
    ((pl.col(f"{ticker}")) * pl.col("JPY=X")).alias(f"{ticker}_JPY")
    # JPY=Xの場合はそのままの終値を使う
    if ticker != "JPY=X"
    else pl.col(f"{ticker}")
    # ティッカーシンボルのリストを使ってループ
    for ticker in tickers
]

df_close = (
    df_close
    # 終値に為替レートを掛け算
    .with_columns(expr_list)
    # JPY=Xの列を削除
    .drop("JPY=X")
    # 空のレコードを削除
    .filter(~pl.all_horizontal(pl.all().is_null()))
)

print(df_close.head())
