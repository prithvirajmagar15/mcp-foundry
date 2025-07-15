# FROM mcr.microsoft.com/devcontainers/python:dev-3.11

# # Install Azure CLI and clean up
# RUN curl -sL https://aka.ms/InstallAzureCLIDeb | bash && \
#     apt-get update && \
#     apt-get install -y azure-cli && \
#     apt-get clean && \
#     rm -rf /var/lib/apt/lists/*

# # Install uv using pipx
# RUN pipx install uv

FROM mcr.microsoft.com/devcontainers/python:dev-3.11

# Install dependencies and Azure CLI
RUN apt-get update && \
    apt-get install -y curl gnupg2 lsb-release software-properties-common && \
    curl -sL https://aka.ms/InstallAzureCLIDeb | bash && \
    apt-get install -y azure-cli && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Install pipx and uv, and ensure its binaries are on PATH
RUN pip install --no-cache-dir pipx && \
    pipx ensurepath && \
    pipx install uv

# Make sure pipx binaries are in PATH
ENV PATH="/root/.local/bin:$PATH"
