#Streamlit app (layout + calls the other files)
import streamlit as st
from indicators import build_price_chart

st.set_page_config(layout="wide")  # uses full browser width, better for a dashboard

st.title("Stock Analysis Dashboard")

ticker_input = st.text_input("Enter a ticker symbol:", value="NVDA")

left_col, right_col = st.columns([1, 1])  # equal width split

from indicators import build_price_chart

with left_col:
    st.subheader("Price Chart & Indicators")
    if ticker_input:
        fig = build_price_chart(ticker_input)
        st.pyplot(fig)

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