import sqlite3
import os
from langchain.tools import tool

DB_PATH = os.path.join(os.path.dirname(__file__), "../mockup_databases/bestbuy_mockup_dataset.sqlite")

#For the time being, we are using best buy playground as I don't have access to a proper best buy api key
#that means this line does nothing at the moment, so commenting out to avoid any issues
#BESTBUY_API_KEY = os.getenv("BESTBUY_API_KEY")

@tool
def search_bestbuy(product_name: str) -> str:
    """Mock: Search BestBuy using the local SQLite Database"""
    #import re
    #import sqlite3

    #match = re.match(r"(.*?)\s+(?:near|in)\s+(\d{5})", query, re.IGNORECASE)
    #if not match:
        #return "Please use the format 'product name near zip code', e.g, 'Iphone near 97360'."
    #product_name, zip_code = match.groups()
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