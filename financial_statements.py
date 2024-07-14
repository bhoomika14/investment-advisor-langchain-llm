import yfinance as yf
import logging
logger = logging.getLogger()
logging.basicConfig(filename='log.txt', encoding='utf-8', level=logging.DEBUG)

# function that gets financial statements of the ticker
def get_financial_statements(ticker):

    company = yf.Ticker(ticker)

    balance_sheet = company.balance_sheet
    balance_sheet.to_csv(f"./data/{ticker}_balance_sheet.csv")

    cash_flow = company.cash_flow
    cash_flow.to_csv(f"./data/{ticker}_cash_flow.csv")

    income_statement = company.income_stmt
    income_statement.to_csv(f"./data/{ticker}_income_statement.csv")

    stock_price_data = yf.download(ticker, period="2y", interval="1d")
    stock_price_data.to_csv(f"./data/{ticker}_stock_price_data.csv")

    return logger.info("Successfully fetched financial statements")


