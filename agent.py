from langchain_openai import OpenAI
from langchain.agents import ZeroShotAgent, AgentExecutor
from langchain.agents.tools import Tool
from ticker_news import get_ticker_news
from financial_statements import get_financial_statements
from prompt import prompt
import json
import os

with open('config.json') as f:
    config = json.load(f)
os.environ['OPENAI_API_KEY'] = config['OPENAI_API_KEY']

#OpenAI - gpt 3.5 turbo
llm = OpenAI(model="gpt-3.5-turbo-instruct", api_key="OPENAI_API_KEY", temperature=0.0)

# creating chain
llm_chain = prompt | llm

# Tools list for agent
tools = [  
    Tool(
        name="Get Recent News",
        func=get_ticker_news,
        description="Useful when you want to obtain information about current financial events."
    ), 
    Tool(
        name = "Get Financial Statements",
        func=get_financial_statements,
        description="Useful when you need to analyze the company's stock price and financial statements to find more insight. Input should be a company ticker such as TSLA for Tesla, NVDA for NVIDIA."
    ),
]

tool_names = [tool.name for tool in tools]

# creating agent
agent = ZeroShotAgent(llm_chain=llm_chain, allowed_tools=tool_names)

agent_executor = AgentExecutor.from_agent_and_tools(agent=agent, tools=tools, verbose=True, max_iterations=2)