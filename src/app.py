import streamlit as st

st.title('Hello World')

# Create input fields
col_ticker, col_weight_1, col_weight_2, col_weight_3 = st.columns(4)  # 4列のコンテナを用意する
with col_ticker:
    ticker = st.text_input("Ticker", value="AAPL")
    ticker2 = st.text_input("Ticker2", value="")
with col_weight_1:
    weight_1 = st.number_input("weight1", value=0)
with col_weight_2:
    weight_2 = st.number_input("weight2", value=0)
with col_weight_3:
    weight_3 = st.number_input("weight3", value=0)

# Button to submit the input
if st.button("Submit"):
    st.write(f"Ticker: {ticker}")
    st.write(f"Weight: {weight_1}")
    st.write(f"Weight: {weight_2}")
    st.write(f"Weight: {weight_3}")