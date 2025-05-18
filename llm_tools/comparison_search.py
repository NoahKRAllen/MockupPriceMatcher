from langchain.tools import Tool
import re
from llm_tools.search_bestbuy import search_bestbuy_tool
from llm_tools.search_target import search_target_tool
from llm_tools.search_walmart import search_walmart_tool


def compare_prices(product_name: str) -> str:
    """Compares product prices across BestBuy, Walmart, and Target."""
    product_name = re.sub(r"(?i)^compare\s+", "", product_name).strip()
    results = []
    for search_fn, store in [
        (search_bestbuy_tool.func, "Best Buy"),
        (search_walmart_tool.func, "Walmart"),
        (search_target_tool.func, "Target"),
    ]:
        try:
            raw_results = search_fn(product_name)

            if isinstance(raw_results, list):
                results.extend(raw_results)


        except Exception as e:
            results.append((f"Error from {search_fn.__name__}", float('inf'), "N/A"))

    if not results:
        return "No product found in any store."

    # Sort and pick top 3 by price
    sorted_results = sorted(results, key=lambda x: x["price"])
    top_three = sorted_results[:3]

    return "Top 3 lowest prices:\n" + "\n".join([f"{item['name']} - ${item['price']:.2f} ({item['store']}) @ {item['url']}" for item in top_three])

compare_prices_search = Tool(
    name = "comparison_search",
    func = compare_prices,
    description = """Compares product prices across BestBuy, Walmart, and Target."""
)