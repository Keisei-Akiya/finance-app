import streamlit as st

from Pages.backtesting_page import backtesting


def main() -> None:
    try:
        backtesting()
    except Exception as e:
        st.write(e)


if __name__ == "__main__":
    main()
