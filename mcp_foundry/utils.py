import requests
from mcp.server.fastmcp import Context
from mcp_foundry.models import ModelsList

def get_client_headers_info(ctx):
    """Get client headers info."""
    client_info = getattr(getattr(ctx.session._client_params, "clientInfo", None), "__dict__", {}) or {}
    client_name = client_info.get("name", "UnknownClient").replace(" ", "-")
    client_version = client_info.get("version", "0.0.0")

    headers = {
        "User-Agent": f"MCP-Client/{client_name} - {client_version}"
    }
    return headers

def get_models_list(ctx: Context, supports_free_playground: bool = None, publisher_name: str = "", license_name: str = "", max_pages: int = 10) -> ModelsList:
    """Get a list of all supported models from Azure AI Foundry with optional filters."""
    url = "https://api.catalog.azureml.ms/asset-gallery/v1.0/models"
    headers = get_client_headers_info(ctx)

    filters = []

    # Always include 'latest' label
    filters.append({"field": "labels", "values": ["latest"], "operator": "eq"})

    if supports_free_playground is not None:
        filters.append({
            "field": "freePlayground",
            "values": ["true" if supports_free_playground else "false"],
            "operator": "contains"
        })

    if publisher_name:
        filters.append({
            "field": "publisher",
            "values": [publisher_name],
            "operator": "contains"
        })

    if license_name:
        filters.append({
            "field": "license",
            "values": [license_name],
            "operator": "contains"
        })

    body = {"filters": filters}

    models_list = {"total_models_count": 0, "fetched_models_count": 0, "summaries": []}

    page_count = 0

    while True and page_count < max_pages:
        page_count += 1
        response = requests.post(url, json=body, headers=headers)
        res_json = response.json()

        print(f"page {page_count} of {max_pages}")

        if "summaries" not in res_json:
            print("Error: 'summaries' not found in the response.")
            break

        models_list["total_models_count"] = res_json.get("totalCount", 0)
        models_list["summaries"].extend(res_json["summaries"])

        # If there are no more pages, break the loop
        if not res_json.get("continuationToken", False):
            print("No more pages to fetch.")
            break

        # Update the body for the next request
        body["continuationToken"] = res_json.get("continuationToken")

    models_list["fetched_models_count"] = len(models_list["summaries"])

    return ModelsList(**models_list)
