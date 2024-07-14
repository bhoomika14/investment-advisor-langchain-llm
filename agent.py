from langchain_community.llms import LlamaCpp
from langchain.agents import ZeroShotAgent, AgentExecutor
from langchain.agents.tools import Tool
from langchain import LLMChain
from ticker_news import get_ticker_news
from financial_statements import get_financial_statements
from prompt import prompt


# LLama as LLM
llm = LlamaCpp(
    model_path="llama-cpp-python/vendor/llama.cpp/models/ggml-vocab-llama-bpe.gguf", max_tokens=256, temperature=0.1, verbose=True
)

# creating agent
llm_chain = LLMChain(
    llm=llm,  
    prompt=prompt 
)

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

agent = ZeroShotAgent(llm_chain=llm_chain, allowed_tools=tool_names)

agent_executor = AgentExecutor.from_agent_and_tools(agent=agent, tools=tools, verbose=True, max_iterations=2)