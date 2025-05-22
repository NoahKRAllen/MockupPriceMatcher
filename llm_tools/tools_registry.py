from llm_tools import search_walmart, search_target, search_bestbuy
import os
import importlib

registered_tools = [search_walmart,search_target,search_bestbuy]

""""
Trimmed this out to try and hunt down and error occurring when trying to refactor over to langgraph instead of langchain 
agents.
# Loop through all .py files in the same directory, except __init__.py
for filename in os.listdir(os.path.dirname(__file__)):
    if filename.endswith(".py") and filename != "__init__.py":
        module_name = filename[:-3]  # Strip .py
        module = importlib.import_module(f"{__name__}.{module_name}")

        # Pull all variables that end in "_tool" from the module
        for attr_name in dir(module):
            if attr_name.endswith("_tool"):
                tool = getattr(module, attr_name)
                registered_tools.append(tool)

if registered_tools is None:
    registered_tools = [search_walmart, search_target, search_bestbuy]
"""