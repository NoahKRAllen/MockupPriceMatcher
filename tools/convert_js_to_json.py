#Scrapped file for now, found that the information we were looking for was in an SQLITE file instead of a JS file

import re
import json

with open("mock_data/product.js", "r") as f:
    js_content = f.read()

#Extract the array
match = re.search(r"export\s+const\s+products\s*=\s*(\[.*\]);?", js_content, re.DOTALL)
if not match:
    raise ValueError("Could not find products array")

array_str = match.group(1)

#Replace single quotes with double quates and fix JS-JSON
array_str = array_str.replace("'", '"')
array_str = re.sub(r"(\w+):", r"\1", array_str) #Add quotes to keys

#Remove any trailing commas
array_str = re.sub(r",\s*}", "}", array_str)
array_str = re.sub(r",\s*]", "}", array_str)

#Parse and save
products = json.loads(array_str)

with open("mock_data/products.json", "w") as f:
    json.dump(products, f, indent = 2)

print("Converted and saved to mock_data/products.json")