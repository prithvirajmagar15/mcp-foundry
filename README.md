# Azure AI Foundry MCP Servers (Experimental)

> **Experimental:** This repository is a playground for evolving Azure AI Foundry capabilities. It empowers Foundry developers to use and extend Foundry as a toolkit for building amazing things. 

[![GitHub watchers](https://img.shields.io/github/watchers/azure-ai-foundry/mcp-foundry.svg?style=social&label=Watch)](https://github.com/azure-ai-foundry/mcp-foundry/watchers)
[![GitHub forks](https://img.shields.io/github/forks/azure-ai-foundry/mcp-foundry.svg?style=social&label=Fork)](https://github.com/azure-ai-foundry/mcp-foundry/fork)
[![GitHub stars](https://img.shields.io/github/stars/azure-ai-foundry/mcp-foundry?style=social&label=Star)](https://github.com/azure-ai-foundry/mcp-foundry/stargazers)
[![Azure AI Community Discord](https://dcbadge.vercel.app/api/server/ByRwuEEgH4)](https://discord.gg/REmjGvvFpW)

## MCP Servers

| Server Name | Description |
|-------------|-------------|
| [Foundry-Agent-Service](./Foundry-Agent-Service/README.md) | Connect to Azure AI Agents and use them in any MCP client. |
| [Foundry-Content-Safety](./Foundry-Content-Safety/README.md) | Content moderation and safety tools for Foundry applications. |
| [Foundry-Knowledge](./Foundry-Knowledge/README.md) | Knowledge management and retrieval for Foundry-powered solutions. |
| [Foundry-Models](./Foundry-Models/README.md) | Model hosting, management, and inference for Foundry. |
| [Foundry-Observability](./Foundry-Observability/README.md) | Monitoring and observability for Foundry services. |

## Access the remote MCP server from any MCP client

All servers in this repository implement the [MCP protocol](https://github.com/modelcontext/model-context-protocol). You can connect to any of these servers from any MCP-compatible client.

**Example:**

1. Obtain the server's endpoint (see the individual server README for details).
2. In your MCP client, configure the remote server URL:
   - For CLI clients: `mcp connect <server-url>`
   - For code: Use the MCP client library to connect to the server endpoint.
3. Interact with the server as per your client's documentation.

Refer to each server's README for specific endpoints, authentication, and usage examples.

## License

This project is licensed under the MIT License. See the LICENSE file for details.

## Contributing

Interested in contributing, and running this server locally? See [CONTRIBUTING.md](./CONTRIBUTING.md) to get started.
