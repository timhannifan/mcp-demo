FROM python:3.13-slim

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    curl && rm -rf /var/lib/apt/lists/*

ARG uv=/root/.local/bin/uv
ADD https://astral.sh/uv/install.sh /install.sh
RUN chmod +x /install.sh && /install.sh && rm /install.sh

# Install ollmcp system-wide so it's available in PATH
RUN $uv pip install --upgrade ollmcp --system

# Keep container running with a dummy command
CMD ["tail", "-f", "/dev/null"]
