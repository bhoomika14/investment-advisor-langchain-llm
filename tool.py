import yfinance as yf
from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage
from langchain.agents import tool
from langchain.agents import AgentExecutor,  create_tool_calling_agent
from langchain_community.document_loaders.web_base import WebBaseLoader
from langchain_community.utilities import GoogleSerperAPIWrapper
import json 
import os
import logging


with open('config.json') as f:
    config = json.load(f)
os.environ["SERPER_API_KEY"] = config['SERPER_API_KEY']
#os.environ['OPENAI_API_KEY'] = config['OPENAI_API_KEY']
os.environ['GOOGLE_API_KEY'] = config['GOOGLE_API_KEY']

logger = logging.getLogger()
logging.basicConfig(filename='log.txt', encoding='utf-8', level=logging.DEBUG)

#function that gets ticker news
@tool
def get_ticker_news(ticker: str):
    """Useful when you want to obtain information about current financial events."""
    links = []
    try:
        # variable that contains all the information about the ticker
        stock = yf.Ticker()

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
        logger.error(f"No news found on Google News about {company}")
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

# function that gets financial statements of the ticker
@tool
def get_financial_statements(ticker: str):
    """Useful when you need to analyze the company's stock price and financial statements to find more insight. Input should be a company ticker such as TSLA for Tesla, NVDA for NVIDIA."""

    company = yf.Ticker(ticker)

    balance_sheet = company.balance_sheet
    balance_sheet.to_csv(f"./data/{ticker}_balance_sheet.csv")

    cash_flow = company.cash_flow
    cash_flow.to_csv(f"./data/{ticker}_cash_flow.csv")

    income_statement = company.income_stmt
    income_statement.to_csv(f"./data/{ticker}_income_statement.csv")

    stock_price_data = yf.download(ticker, period="2y", interval="1d")
    stock_price_data.to_csv(f"./data/{ticker}_stock_price_data.csv")

    return balance_sheet, cash_flow, income_statement, stock_price_data

# Run the agent with a query
template = """
As a stock analyst, provide investment insights based on the company's financial performance and market trends. 
Avoid direct 'Buy' or 'Sell' recommendations. Use your database to create a detailed investment thesis.

Use the following format:
News Insights: Share recent news insights with the specific time frame.

Balance Sheet Analysis: Analyze the balance sheet for the specified period.

Cash Flow Analysis: Analyze cash flow for the specified period.

Income Statement Analysis: Analyze the income statement for the specified period.

Summary: Provide a final answer backed by the above analysis, mentioning the specific time frame.

Encourage further research and consideration of various factors before making investment decisions.

At the end add a line 'Investments are subject to market risk. Please read all scheme related documents carefully before investing.'

Begin!

{input}
{agent_scratchpad}

"""
#prompt = PromptTemplate(input_variables=["input", "agent_scratchpad"], template=template)
prompt = ChatPromptTemplate.from_messages([
    ("system", template),
    MessagesPlaceholder("chat_history", optional=True),
    ("human", "{input}"),
    MessagesPlaceholder("agent_scratchpad"),
])

llm = ChatGoogleGenerativeAI(model="gemini-pro", temperature=0.0, convert_system_message_to_human=True, max_output_tokens=800)

tools = [get_ticker_news, get_financial_statements]
llm_with_tools = llm.bind_tools(tools)

agent = create_tool_calling_agent(llm, [get_ticker_news, get_financial_statements], prompt)

agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)



# # Tools list for agent
# tools = [  
#     Tool(
#         name="Get Recent News",
#         func=get_ticker_news,
#         description="Useful when you want to obtain information about current financial events."
#     ), 
#     Tool(
#         name = "Get Financial Statements",
#         func=get_financial_statements,
#         description="Useful when you need to analyze the company's stock price and financial statements to find more insight. Input should be a company ticker such as TSLA for Tesla, NVDA for NVIDIA."
#     ),
# ]

# functions = [convert_to_openai_function(t) for t in tools]

# message = llm.invoke(
#     [HumanMessage(content="move file foo to bar")], functions=functions
# )

# print(message)

# tool = [get_ticker_news("TSLA")]
# functions = [convert_to_openai_function(t) for t in tool]

# tools = [get_financial_statements, get_ticker_news]
# functions = [convert_to_openai_function(t) for t in tool]

# # creating agent
# agent = create_openai_functions_agent(llm, tools, prompt)
# #agent = initialize_agent(tools=tools, llm=llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION)
# agent_executor = AgentExecutor.from_agent_and_tools(agent=agent, tools=tools, max_iterations=2)


# result = agent_executor.invoke({"input":"Provide an investement analysis on TSLA"}, functions=functions)
