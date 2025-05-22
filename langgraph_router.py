from langgraph.graph import StateGraph
from langgraph.prebuilt.tool_node import ToolNode
from langchain_ollama.llms import OllamaLLM
from llm_tools.comparison_search import compare_prices_tool
from llm_tools.multi_shop_search import multi_shop_tool

llm=OllamaLLM(model="gemma3")


def smart_router(input: dict) -> str:
    user_input = input["user_input"]
    prompt = f"""
You are a router for a shopping assistant.

Available tools:
- multi_shop_search: Use this to search all stores for a product:
- compare_prices_search: Use this if the user wants to compare prices between stores.

Decide which tool to use for the user's request.

User input: {user_input}

Respond ONLY with the tool name: either 'multi_shop_search' or 'compare_prices_search'.
"""
    response = llm.invoke(prompt).strip().lower()
    print(f"[Router Decision] '{user_input}' -> {response}")
    return response


# LangGraph Setup
class GraphState(dict):
    pass


graph = StateGraph(GraphState)
graph.add_node("search", ToolNode(multi_shop_tool))
graph.add_node("compare", ToolNode(compare_prices_tool))
graph.add_node("route", smart_router)

graph.set_entry_point("route")
graph.add_edge("route", "search", condition=lambda x: smart_router(x) == "multi_shop_search")
graph.add_edge("route", "compare", condition=lambda x: smart_router(x) == "compare_prices_search")
graph.set_finish_point("search")
graph.set_finish_point("compare")

final_graph = graph.compile()

def run_router(input_text):
    return final_graph.invoke({"input" : input_text})