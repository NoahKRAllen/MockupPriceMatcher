from langchain.tools import Tool
import re
from llm_tools import tools

def compare_prices(product_name: str) -> str:
    """Compares product prices across BestBuy, Walmart, and Target and returns the top 10 options."""
    product_name = re.sub(r"(?i)^compare\s+", "", product_name).strip()
    results = []
    for search_fn in tools:
        try:
            raw_results = search_fn(product_name)


            if isinstance(raw_results, list):
                results.extend(raw_results)


        except Exception as e:
            results.append((f"Error from {search_fn.__name__}", float('inf'), "N/A"))

    if not results:
        return "No product found in any store."

    # Sort and pick top 10 by price
    sorted_results = sorted(results, key=lambda x: x["price"])
    top_ten = sorted_results[:10]

    return "Top 10 lowest prices:\n" + "\n".join([f"{item['name']} - ${item['price']:.2f} @ ({item['store']}) {item['url']}" for item in top_ten])

compare_prices_search = Tool(
    name = "comparison_search",
    func = compare_prices,
    description = """Compares product prices across BestBuy, Walmart, and Target and returns the top 10 options."""
)