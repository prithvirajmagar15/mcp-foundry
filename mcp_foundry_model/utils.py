import requests
from mcp.server.fastmcp import Context
from mcp_foundry_model.models import ModelsList
import os
import dotenv

dotenv.load_dotenv()

labs_api_url = os.environ.get("LABS_API_URL", "https://labs-mcp-api.azurewebsites.net/api/v1")

def get_client_headers_info(ctx):
    """Get client headers info."""
    client_info = getattr(
        getattr(ctx.session._client_params, "clientInfo", None), "__dict__", {}) or {}
    client_name = client_info.get("name", "UnknownClient").replace(" ", "-")
    client_version = client_info.get("version", "0.0.0")

    headers = {
        "User-Agent": f"MCP-Client/{client_name} - {client_version}"
    }
    return headers
 
def get_models_list(ctx: Context, supports_free_playground: bool = None, publisher_name: str = "", license_name: str = "", 
                    max_pages: int = 5, model_name: str = None) -> ModelsList:
    """Get a list of all supported models from Azure AI Foundry with optional filters."""
    url = "https://api.catalog.azureml.ms/asset-gallery/v1.0/models"
    headers = get_client_headers_info(ctx)

    filters = []

    # Always include 'latest' label
    filters.append({"field": "labels", "values": ["latest"], "operator": "eq"})

    if supports_free_playground is True:
        filters.append({
            "field": "freePlayground",
            "values": ["true"],
            "operator": "eq"
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

    if model_name:
        filters.append({
            "field": "name",
            "values": [model_name],
            "operator": "eq"
        })

    body = {"filters": filters}

    models_list = {"total_models_count": 0,
                   "fetched_models_count": 0, "summaries": []}

    page_count = 0

    while True and page_count < max_pages:
        page_count += 1
        response = requests.post(url, json=body, headers=headers)
        res_json = response.json()

        if "summaries" not in res_json:
            break

        for summary in res_json["summaries"]:
            summary["deployment_options"] = {
                "openai": False,
                "serverless_endpoint": False,
                "managed_compute": False,
                "free_playground": False,
            }

            if "playgroundLimits" in summary:
                summary["deployment_options"]['free_playground'] = True

            publisher = summary.get("publisher", "")
            if publisher and publisher.lower() == "openai":
                summary["deployment_options"]['openai'] = True
            else:
                if "standard-paygo" in summary.get("azureOffers"):
                    summary["deployment_options"]['serverless_endpoint'] = True
                if "VM" in summary.get("azureOffers") or "VM-withSurcharge" in summary.get("azureOffers"):
                    summary["deployment_options"]['managed_compute'] = True

        models_list["total_models_count"] = res_json.get("totalCount", 0)
        models_list["summaries"].extend(res_json["summaries"])

        # If there are no more pages, break the loop
        if not res_json.get("continuationToken", False):
            break

        # Update the body for the next request
        body["continuationToken"] = res_json.get("continuationToken")

    models_list["fetched_models_count"] = len(models_list["summaries"])

    return ModelsList(**models_list)

async def get_code_sample_for_github_model(publisher_name: str, model_name: str, ctx: Context) -> str:
    headers = get_client_headers_info(ctx)

    response = requests.get(f"{labs_api_url}/resources/resource/gh_guidance.md", headers=headers)
    if response.status_code != 200:
        return f"Error fetching projects from API: {response.status_code}"

    guidance = response.json()
    GH_GUIDANCE = guidance["resource"]["content"]

    guidance = GH_GUIDANCE.replace("{{inference_model_name}}", f"{publisher_name}/{model_name}")

    return guidance

async def get_code_sample_for_labs_model(model_name: str, ctx: Context) -> str:
    headers = get_client_headers_info(ctx)

    response = requests.get(f"{labs_api_url}/projects/{model_name}/implementation", headers=headers)
    if response.status_code != 200:
        return f"Error fetching projects from API: {response.status_code}"

    project_response = response.json()

    return project_response['project']

async def  get_code_sample_for_deployment_under_ai_services() -> str:
    """
    Retrieves code samples for deploying models under Azure AI Services.

    This function is used to get code examples and implementation instructions for deploying models in Azure AI Services, helping users understand how to integrate and use the models effectively in their applications.

    Returns:
        str: A string containing the code samples and usage instructions for deploying models under Azure AI Services.
    """

    pass

async def get_ai_services_usage_list(ctx: Context) -> str:
    """
    Retrieves a list of usage examples for Azure AI Services.

    This function is used to get examples of how to use Azure AI Services, helping users understand the various applications and use cases for the services.

    Returns:
        str: A string containing the usage examples for Azure AI Services.
    """

    headers = get_client_headers_info(ctx)

    pass