from pydantic import BaseModel


class ModelsList(BaseModel):
    """
    Model to store the list of models in the MCP Foundry.
    """
    total_models_count: int
    fetched_models_count: int
    summaries: list[dict]