FROM python:3.12-slim

# Install pandoc and clean up apt cache in a single layer
RUN apt-get update \
    && apt-get install -y --no-install-recommends pandoc \
    && rm -rf /var/lib/apt/lists/*

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /usr/local/bin/

WORKDIR /app

# Copy the parent package first (required by server.py imports)
COPY setup.py README.md LICENSE ./
COPY pypandoc_hwpx/ pypandoc_hwpx/

# Install the parent package
RUN uv pip install --system -e .

# Copy MCP server project files and sync dependencies
COPY mcp/pyproject.toml mcp/uv.lock mcp/.python-version mcp/
WORKDIR /app/mcp
RUN uv sync --frozen --no-dev

# Copy MCP server source
COPY mcp/server.py .

# Default: stdio transport; pass --http [--port PORT] for Streamable HTTP
ENTRYPOINT ["uv", "run", "server.py"]
CMD []
