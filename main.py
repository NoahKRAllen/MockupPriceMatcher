from langchain.agents import initialize_agent, AgentType
from langchain_ollama.llms import OllamaLLM
from llm_tools import tools
from llm_tools.comparison_search import compare_prices_search

llm = OllamaLLM(model="gemma3")

single_search_agent = initialize_agent(
    tools=tools,
    llm=llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True,
)

compare_search_agent = initialize_agent(
    tools=[compare_prices_search],
    llm=llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True,
)

if __name__ == "__main__":
    query = input("What product are you looking for? ")

    if "compare" in query.lower():
        response = compare_prices_search(query)
    else:
        response = single_search_agent(query)

    print(response)