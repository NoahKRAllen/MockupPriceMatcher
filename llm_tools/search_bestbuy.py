import sqlite3
import os
from langchain.tools import Tool

DB_PATH = os.path.join(os.path.dirname(__file__), "../mockup_databases/bestbuy_mockup_dataset.sqlite")

#For the time being, we are using best buy playground as I don't have access to a proper best buy api key
#that means this line does nothing at the moment, so commenting out to avoid any issues
#BESTBUY_API_KEY = os.getenv("BESTBUY_API_KEY")

def search_bestbuy(product_name: str) -> str:
    """Search BestBuy using the local SQLite Database"""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        query = """
                SELECT name, price, url FROM products
                WHERE name LIKE ? COLLATE NOCASE
                ORDER BY price ASC
                LIMIT 5;
                """

        cursor.execute(query, (f"%{product_name}%",))
        results = cursor.fetchall()

        if not results:
            return f"No products found for '{product_name}'"

        response = "Top results:\n"
        for name, price, url in results:
            response += f"- {name} | ${price} | URL: {url}\n"

        return response.strip()

    except Exception as e:
        return f"Error querying database: {str(e)}"

    finally:
        if conn:
            conn.close()

search_bestbuy_tool = Tool(
    name = "search_bestbuy",
    func = search_bestbuy,
    description = """Search BestBuy using the local SQLite Database and return the name, price, and mock URL for the items"""
)