from langchain.agents import initialize_agent, AgentType
from langchain_ollama.llms import OllamaLLM
from llm_tools import tools

llm = OllamaLLM(model="gemma3")

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