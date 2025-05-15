import importlib
import os
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("azure-ai-foundry-mcp-server")

def auto_import_modules(base_package: str, targets: list[str]):
    """
    Automatically imports specified Python modules (e.g., tools.py, resources.py, prompts.py)
    from each subpackage of base_package.
    """
    package = importlib.import_module(base_package)
    package_path = package.__path__[0]

    for submodule in os.listdir(package_path):
        sub_path = os.path.join(package_path, submodule)

        if not os.path.isdir(sub_path) or submodule.startswith("__"):
            continue

        for target in targets:
            module_name = f"{base_package}.{submodule}.{target}"
            try:
                importlib.import_module(module_name)
                print(f"✅ Imported: {module_name}")
            except ModuleNotFoundError:
                print(f"⚠️ Skipping {module_name} (not found)")
            except Exception as e:
                print(f"❌ Error importing {module_name}: {e}")

# Run this on startup
auto_import_modules("mcp_foundry", targets=["tools", "resources", "prompts"])
