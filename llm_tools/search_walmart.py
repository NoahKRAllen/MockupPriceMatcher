import sqlite3
import os
from langchain.tools import Tool

DB_PATH = os.path.join(os.path.dirname(__file__), "../mockup_databases/walmart_mockup_dataset.sqlite")

#For the time being, we are using best buy playground as I don't have access to a proper best buy api key
#that means this line does nothing at the moment, so commenting out to avoid any issues
#WALMART_API_KEY = os.getenv("WALMART_API_KEY")

def search_walmart(product_name: str) -> str | list[dict]:
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        query = """
                SELECT name, price, url FROM products
                WHERE name LIKE ? COLLATE NOCASE
                ORDER BY price ASC
                LIMIT 3;
                """

        cursor.execute(query, (f"%{product_name}%",))
        results = cursor.fetchall()

        if not results:
            return f"No products found for '{product_name}'"

        store = "Walmart"
        structured_results = []
        for name, price, url in results:
            structured_results.append({
                "store": store,
                "name": name,
                "price": price,
                "url": url
            })
        return structured_results

    except Exception as e:
        return f"Error querying database: {str(e)}"

    finally:
        if conn:
            conn.close()

search_walmart_tool = Tool(
    name = "search_walmart",
    func = search_walmart,
    description = """Search Walmart using the local SQLite Database and return the name, price, and mock URL for the items"""
)