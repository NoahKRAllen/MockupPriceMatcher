import os
import importlib

tools = []

# Loop through all .py files in the same directory, except __init__.py
for filename in os.listdir(os.path.dirname(__file__)):
    if filename.endswith(".py") and filename != "__init__.py":
        module_name = filename[:-3]  # Strip .py
        module = importlib.import_module(f"{__name__}.{module_name}")

        # Pull all variables that end in "_tool" from the module
        for attr_name in dir(module):
            if attr_name.endswith("_tool"):
                tool = getattr(module, attr_name)
                tools.append(tool)
