FROM python:3.13-slim

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc curl && rm -rf /var/lib/apt/lists/*

ARG uv=/root/.local/bin/uv
ADD https://astral.sh/uv/install.sh /install.sh
RUN chmod +x /install.sh && /install.sh && rm /install.sh

COPY requirements.txt ./
RUN $uv pip install --no-cache-dir -r requirements.txt --system

COPY . .

ENV MCP_HOST=0.0.0.0
ENV MCP_PORT=8765

CMD ["python", "app.py"]
