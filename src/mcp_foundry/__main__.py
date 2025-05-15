import logging
from .mcp_server import mcp

# Configure logger
logger = logging.getLogger("mcp_foundry")
logging.basicConfig(level=logging.DEBUG)

def main() -> None:
    """Runs the MCP server"""
    print("Starting MCP server")
    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
