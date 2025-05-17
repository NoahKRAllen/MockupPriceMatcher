from langchain.agents import initialize_agent, AgentType
from langchain_ollama.llms import OllamaLLM
from tools.mock_bestbuy_tool import search_bestbuy

llm = OllamaLLM(model="gemma3")
tools = [search_bestbuy]

agent = initialize_agent(
    tools=tools,
    llm=llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True,
)

if __name__ == "__main__":
    query = input("What product are you looking for? ")
    response = agent.run(f"Find {query}")
    print(response)