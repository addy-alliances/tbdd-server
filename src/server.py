import importlib
import pkgutil
from pathlib import Path

import src.tools as tools_pkg
from src.mcp_app import mcp


def load_tool_modules():
    root = Path(tools_pkg.__file__).resolve().parent
    for module_info in pkgutil.walk_packages([str(root)], prefix=f"{tools_pkg.__name__}."):
        module = importlib.import_module(module_info.name)
        _ = module


load_tool_modules()


if __name__ == "__main__":
    mcp.run(transport="http", port=8000)