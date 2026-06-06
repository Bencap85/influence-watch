FROM python:3.11-slim AS base

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Create non-root user
RUN useradd -m mcpuser

# Set working directory
WORKDIR /app

# Copy dependency file
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy ALL backend code into the image
COPY ./shared ./shared
COPY ./mcp ./mcp

# Switch to non-root user
USER mcpuser

# Expose MCP port
EXPOSE 9000

# Run the MCP server
CMD ["uvicorn", "mcp.mcp_http_server:app", "--host", "0.0.0.0", "--port", "9000"]
