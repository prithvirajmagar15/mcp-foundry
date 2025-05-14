import importlib
import os
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("azure-ai-foundry-mcp-server")

def auto_import_tools_modules(base_package: str):
    """
    Automatically imports `tools.py` from each subpackage of base_package
    """
    package = importlib.import_module(base_package)
    package_path = package.__path__[0]

    for submodule in os.listdir(package_path):
        sub_path = os.path.join(package_path, submodule)

        if not os.path.isdir(sub_path) or submodule.startswith("__"):
            continue

        tools_module = f"{base_package}.{submodule}.tools"
        try:
            importlib.import_module(tools_module)
            print(f"✅ Imported: {tools_module}")
        except ModuleNotFoundError:
            print(f"⚠️ Skipping {tools_module} (not found)")
        except Exception as e:
            print(f"❌ Error importing {tools_module}: {e}")

# Run this on startup
auto_import_tools_modules("mcp_foundry")