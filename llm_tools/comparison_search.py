﻿from langchain.tools import Tool
import re
from llm_tools.tools_registry import registered_tools

def compare_prices(product_name: str) -> str:
    """Compares product prices across BestBuy, Walmart, and Target and returns the top 10 options."""
    product_name = re.sub(r"(?i)^compare\s+", "", product_name).strip().strip('"\'`()')
    results = []
    for search_fn in registered_tools:
        try:
            raw_results = search_fn(product_name)


            if isinstance(raw_results, list):
                results.extend(raw_results)


        except Exception as e:
            results.append({
                "name": f"Error from {search_fn.__name__}: {str(e)}",
                "price": float('inf'),
                "store": "N/A",
                "url": "N/A"
            })

    if not results:
        return "No product found in any store."

    # Sort and pick top 10 by price
    sorted_results = sorted(results, key=lambda x: x["price"])
    top_ten = sorted_results[:10]

    return "Top 10 lowest prices:\n" + "\n".join([f"{item['name']} - ${item['price']:.2f} @ ({item['store']}) {item['url']}" for item in top_ten])

compare_prices_tool = Tool(
    name = "compare_prices_search_tool",
    func = compare_prices,
    description =
        "Use this tool when the user wants to compare prices for a product across multiple retailers. "
        "It searches BestBuy, Walmart, and Target, then returns the top 10 cheapest options. "
        "The input should be a product name, like 'iPhone' or 'Bluetooth headphones'."
)