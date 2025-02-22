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

# polars.exprを使って為替レートを掛け算
# 例えば、VOOの終値にJPY/USDの為替レートを掛け算して、JPYでの終値を計算する
# ただし、JPY=Xの場合は為替レートを掛け算しない
expr_list = [
    ((pl.col(f"{ticker}")) * pl.col("JPY=X")).alias(f"{ticker}_JPY") if ticker != "JPY=X" else pl.col(f"{ticker}")
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
