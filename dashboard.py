#Streamlit app (layout + calls the other files)
import streamlit as st

st.set_page_config(layout="wide")  # uses full browser width, better for a dashboard

st.title("Stock Analysis Dashboard")

ticker_input = st.text_input("Enter a ticker symbol:", value="AAPL")

left_col, right_col = st.columns([1, 1])  # equal width split

with left_col:
    st.subheader("Price Chart & Indicators")
    st.write("Placeholder: price chart, Bollinger Bands, MAs, RSI, Volume")

with right_col:
    with st.container(border=True):
        st.subheader("Valuation & Fundamentals")
        st.write("Placeholder: current price, earnings, % measures, DCF + WACC, multiples")

    with st.container(border=True):
        st.subheader("M&A Suggestions")
        st.write("Placeholder: sector/market-cap based suggestions + reasoning")

    with st.container(border=True):
        st.subheader("Macro & Sector News")
        st.write("Placeholder: global macro news, sector-specific news")