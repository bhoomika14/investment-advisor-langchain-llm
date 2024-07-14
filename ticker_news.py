import yfinance as yf
from langchain_community.document_loaders.web_base import WebBaseLoader
from langchain_community.utilities import GoogleSerperAPIWrapper
import json 
import os
import logging

with open('config.json') as f:
    config = json.load(f)
os.environ["SERPER_API_KEY"] = config['SERPER_API_KEY']
logger = logging.getLogger()
logging.basicConfig(filename='log.txt', encoding='utf-8', level=logging.DEBUG)

#function that gets ticker news
def get_ticker_news(ticker):
    links = []
    try:
        # variable that contains all the information about the ticker
        stock = yf.Ticker(ticker)

        # getting link from stock news
        links = [n['link'] for n in stock.news if n['type'] == "STORY"]
        print("Links stored successfully")
    except Exception as e:
        print(e)
    
    # get the company full name
    company = stock.info['longName']

    # search in the Google News about the company or ticker
    search = GoogleSerperAPIWrapper(type="news", tbs="qdr:d5", serper_api_key=os.environ["SERPER_API_KEY"])
    results = search.results(f"financial news about {company} or {ticker}")
    print("News found in Google News")
    if not results['news']:
        logger.error(f"No new found on Google News about {company}")
    else:
        for i, item in zip(range(3), results['news']):
            try:
                links.append(item['link'])
                print(f"{len(links)} links stored about {company}")
            except Exception as e:
                print(e)

    loader = WebBaseLoader(links)
    docs = loader.load()
    title_content = []
    for doc in docs:
        title = doc.metadata.get('title', 'No title available')
        page_content = doc.page_content.strip() if ticker in doc.page_content else ""
        title_text = f"{title}:{page_content}\n"
        title_content.append(title_text)
    data = "\n".join(title_content)
    return data

