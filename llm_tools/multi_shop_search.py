from langchain.tools import Tool
from llm_tools.tools_registry import registered_tools
import re
def multi_shop(product_name: str) -> str:
    """Finds product prices across BestBuy, Walmart, and Target and returns the top three options from each shop."""
    #Strip the input to grab the specific name of the product
    product_name = re.sub(r'(?i)^product_name\s*=\s*', '', product_name).strip().strip('"\'`()')
    print("Searching for: ", product_name)
    results = []
    for search_fn in registered_tools:
        try:
            raw_results = search_fn(product_name)
            #Find the top three of a shop, add it to a results
            if isinstance(raw_results, list):
                sorted_results = sorted(raw_results, key=lambda x: x["price"])
                top_three = sorted_results[:3]
                results.extend(top_three)


        except Exception as e:
            results.extend({
                "name": f"Error from {search_fn.__name__}: {str(e)}",
                "price": float('inf'),
                "store": "N/A",
                "url": "N/A"
            })

    if not results:
        return "No product found in any store."

    return "Top 3 lowest prices in each store:\n" + "\n".join(
        [f"{item['name']} - ${item['price']:.2f} @ ({item['store']}) {item['url']}" for item in results])

multi_shop_tool = Tool(
    name = "multi_shop_search_tool",
    func = multi_shop,
    description = """Finds product prices across BestBuy, Walmart, and Target and returns the top 3 options from each store."""
)