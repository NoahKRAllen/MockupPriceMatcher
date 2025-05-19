from langchain.agents import initialize_agent, AgentType
from langchain_ollama.llms import OllamaLLM
from llm_tools.comparison_search import compare_prices_search
from llm_tools.multi_shop_search import multi_shop_search
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler

llm = OllamaLLM(model="gemma3")

multi_shop_agent = initialize_agent(
    tools=[multi_shop_search],
    llm=llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True
)

compare_search_agent = initialize_agent(
    tools=[compare_prices_search],
    llm=llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True
)

if __name__ == "__main__":
    query = input("What product are you looking for? ")

    if "compare" in query.lower():
        response = compare_search_agent.run(query)
    else:
        response = multi_shop_agent.run(query)

    print(response)