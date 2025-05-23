from langgraph.graph import StateGraph
from langgraph.prebuilt.tool_node import ToolNode
from langchain_ollama.llms import OllamaLLM
from llm_tools.comparison_search import compare_prices
from llm_tools.multi_shop_search import multi_shop
from pydantic import BaseModel

llm=OllamaLLM(model="gemma3")


def smart_router(input_model) -> str:
    print("[DEBUG] input_dict passed to smart_router:", input_model)

    user_input_str = input_model.user_input
    if not user_input_str:
        print("[WARNING] No 'user_input_str' found!")
    prompt = f"""
You are a router for a shopping assistant.

Available tools:
- multi_shop_search: Use this to search all stores for a product:
- compare_prices_search: Use this if the user wants to compare prices between stores.

Decide which tool to use for the user's request.

User input: {user_input_str}

Respond ONLY with the tool name: either 'multi_shop_search' or 'compare_prices_search'.
"""
    response = llm.invoke(prompt).strip().lower()
    print(f"[Router Decision] '{user_input_str}' -> {response}")
    return response


# LangGraph Setup
class GraphState(BaseModel):
    user_input: str = ""
    result: str = ""

multi_shop_tool_node = ToolNode([multi_shop])
compare_prices_tool_node = ToolNode([compare_prices])

graph = StateGraph(GraphState)
graph.add_node("search", multi_shop_tool_node)
graph.add_node("compare", compare_prices_tool_node)
graph.add_node("route", smart_router)

graph.set_entry_point("route")
graph.add_conditional_edges("route", path=smart_router, path_map={
    "multi_shop_search": "search",
    "compare_prices_search": "compare"
})


graph.set_finish_point("search")
graph.set_finish_point("compare")

final_graph = graph.compile()

def run_router(input_text):
    print("[DEBUG] input_dict passed to smart_router:", input_text)
    return final_graph.invoke(GraphState(user_input=input_text))