from langchain_ollama.llms import OllamaLLM
from langgraph_router import run_router

llm = OllamaLLM(model="gemma3")

"""
Trimmed out in preparation for moving to LangGraph instead of individual agents
multi_shop_agent = initialize_agent(
    tools=[multi_shop_tool],
    llm=llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True
)

compare_search_agent = initialize_agent(
    tools=[compare_prices_tool],
    llm=llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True
)
"""
def main():
    while True:
        query = input("What can I help you with?")
        print("[DEBUG] input_dict passed to smart_router:", query)
        if query.lower() in ["exit", "quit", "close"]:
            break

        response = run_router(query)
        print(response["result"])


if __name__ == "__main__":
    main()