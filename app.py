import streamlit as st
from tool import agent_executor
st.set_page_config(page_title="Investment Advisor Tool", page_icon=":moneybag:", layout="wide", initial_sidebar_state="collapsed")

st.markdown(
    f"""
    <style>
    .stApp {{
        background-image: url("https://img.freepik.com/free-photo/growth-economy-with-coins-concept_23-2148525276.jpg?t=st=1721884969~exp=1721888569~hmac=135fdc20f02a06532a39618b0b8e51e3ae19d0e25aba4f560a3e0f31d6e269bd&w=1060");
        background-size: cover;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }}
    </style>
    """,
    unsafe_allow_html=True
)

col1, col2 = st.columns((0.8, 0.3), vertical_alignment="center")
with col1.container():
    st.title("Investment advisor tool")
    st.subheader("Smart Insights for Smart Investments!💸")
    stock_codes = {
    "Apple Inc.": "AAPL",
    "Microsoft Corporation": "MSFT",
    "Amazon.com, Inc.": "AMZN",
    "Alphabet Inc. (Class A)": "GOOGL",
    "Alphabet Inc. (Class C)": "GOOG",
    "Facebook, Inc. (Meta Platforms)": "META",
    "Tesla, Inc.": "TSLA",
    "Berkshire Hathaway Inc. (Class A)": "BRK.A",
    "Berkshire Hathaway Inc. (Class B)": "BRK.B",
    "Johnson & Johnson": "JNJ",
    "Visa Inc.": "V",
    "JPMorgan Chase & Co.": "JPM",
    "Walmart Inc.": "WMT",
    "Procter & Gamble Co.": "PG",
    "NVIDIA Corporation": "NVDA",
    "Mastercard Incorporated": "MA",
    "Disney (The Walt Disney Company)": "DIS",
    "PayPal Holdings, Inc.": "PYPL",
    "Netflix, Inc.": "NFLX",
    "Intel Corporation": "INTC"}

    with st.container():
        ticker = st.selectbox(":bold[Select a stock]", stock_codes.keys(), index=None)
        if ticker is not None:
            ticker_str = stock_codes[ticker]
            result = agent_executor.invoke({"input": f"Provide analysis on {ticker_str}"})

            with st.container(border=True):
                st.write(f":bold[Here's the recent information you should know about {ticker}]")
                st.markdown(f"{result['output']}")
        
        
    
    