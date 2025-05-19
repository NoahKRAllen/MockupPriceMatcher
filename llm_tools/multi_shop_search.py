from langchain.tools import Tool
from llm_tools import tools
import re
def multi_shop(product_name: str) -> str:
    """Finds product prices across BestBuy, Walmart, and Target and returns the top three options from each shop."""

    product_name = re.sub(r'(?i)^product_name\s*=\s*', '', product_name).strip().strip('"')
    results = []
    for search_fn in tools:
        try:
            raw_results = search_fn(product_name)

            if isinstance(raw_results, list):
                sorted_results = sorted(raw_results, key=lambda x: x["price"])
                top_three = sorted_results[:3]
                results.extend(top_three)


        except Exception as e:
            results.append((f"Error from {search_fn.__name__}", float('inf'), "N/A"))

    if not results:
        return "No product found in any store."

    return "Top 3 lowest prices in each store:\n" + "\n".join([f"{item['name']} - ${item['price']:.2f} @ ({item['store']}) {item['url']}" for item in results])

multi_shop_search = Tool(
    name = "multi_shop_search",
    func = multi_shop,
    description = """Finds product prices across BestBuy, Walmart, and Target and returns the top 3 options from each store."""
)