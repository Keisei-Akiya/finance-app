# ライブラリのインポート
import polars as pl
import yfinance as yf

tickers = ['VOO', 'VGK', 'JPY=X']

yf_tickers = yf.Tickers(tickers=tickers)
historical_data = yf_tickers.history(period='1wk')

df_close = pl.DataFrame(historical_data['Close'])

# polars.exprを使って為替レートを掛け算
# 例えば、VOOの終値にJPY/USDの為替レートを掛け算して、JPYでの終値を計算する
# ただし、JPY=Xの場合は為替レートを掛け算しない
expr_list = [
    ((pl.col(f'{ticker}')) * pl.col('JPY=X')).alias(f'{ticker}_JPY')
    if ticker != 'JPY=X' else pl.col(f'{ticker}')
    for ticker in tickers
]
df_close = df_close.with_columns(expr_list)

print(df_close.head())