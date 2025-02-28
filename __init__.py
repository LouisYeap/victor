import glob
import os

modules = glob.glob(os.path.join(os.path.dirname(__file__), "*.py"))

for module in modules:
    if os.path.isfile(module) and not module.endswith("__init__.py"):
        module_name = os.path.basename(module)[:-3]
        exec(f"from .{module_name} import *")
