# ScholarLens MCP Demo

A demonstration of the Model Context Protocol (MCP) featuring an academic retrieval and text analytics server with a Python client. This project showcases how to build and deploy MCP tools for document search, question answering, and text analysis.

## Features

- **Corpus Answer Tool**: Query a local corpus of academic documents and get synthesized answers with citations
- **Text Profile Tool**: Analyze text documents for readability, sentiment, and linguistic features
- **Docker-based Deployment**: Containerized server and client for easy setup and testing
- **FastMCP Integration**: Built on the FastMCP framework for rapid MCP tool development

## Architecture

The project consists of two main components:

- **MCP Server** (`server/`): A FastMCP-based server that exposes two tools and serves academic documents
- **MCP Client** (`client/`): A Python client that demonstrates how to interact with the MCP server

## Project Structure

```markdown:README.md
mcp-demo/
├── client/                 # MCP client implementation
│   ├── Dockerfile         # Client container configuration
│   ├── mcp_client_smoke.py # Demo client script
│   ├── requirements.txt   # Python dependencies
│   └── scripts/           # Utility scripts
├── server/                 # MCP server implementation
│   ├── app.py             # Main server application
│   ├── schemas.py         # Pydantic data models
│   ├── tools/             # MCP tool implementations
│   │   ├── corpus_answer.py    # Document search and Q&A
│   │   └── text_profile.py     # Text analytics
│   ├── data/corpus/       # Sample academic documents
│   └── requirements.txt   # Python dependencies
├── docker-compose.yml     # Multi-container orchestration
└── Makefile              # Development commands
```

##  Quick Start

### 1. Start the Services

```bash
# Build and run both server and client
make up

# Or for development with localhost access
make dev
```

### 2. View Logs

```bash
make logs
```

### 3. Stop Services

```bash
make down
```

## Development Commands

```bash
# Rebuild containers from scratch
make rebuild

# Run only the client
make client

# Access server shell
make server-sh

# Access client shell
make client-sh

# Clean up containers and volumes
make clean
```

## Available Tools

### 1. Corpus Answer Tool

Answers questions using a local corpus of academic documents:

```python
# Example query
result = await client.call_tool(
    "corpus_answer_tool",
    {"query": "How do urban transport policies affect emissions and health?"}
)
```

**Returns**: `AnswerWithCitations` with:
- Synthesized answer (≤120 words)
- 1-5 supporting sources with snippets and similarity scores

### 2. Text Profile Tool

Analyzes text documents for various linguistic features:

```python
# Analyze a document by ID or raw text
result = await client.call_tool(
    "text_profile_tool",
    {"text_or_doc_id": "air_quality_health.txt"}
)
```

**Returns**: `TextProfile` with:
- Character and token counts
- Type-token ratio (lexical diversity)
- Top n-grams and keywords
- Flesch reading ease score
- VADER sentiment analysis

##  Sample Corpus

The server includes three sample academic documents:
- `ai_labor_markets.txt` - AI's impact on employment
- `air_quality_health.txt` - Air pollution and public health
- `urban_transport_emissions.txt` - Urban transportation and emissions

## API Endpoints

- **MCP Tools**: Available at `/mcp` (MCP protocol)
- **Health Check**: `GET /health` - Returns "OK" for container health checks

## How It Works

1. **Server Startup**: The MCP server loads the corpus and builds a TF-IDF index for semantic search
2. **Client Connection**: The client waits for the server to be healthy, then connects via HTTP transport
3. **Tool Execution**: Tools process requests using scikit-learn for text analysis and similarity search
4. **Response Format**: All responses use Pydantic models for type safety and validation

## Docker Configuration

- **Server**: Exposes port 8765 internally, with optional localhost binding for development
- **Client**: Waits for server health check before running the demo
- **Volumes**: Corpus data is mounted from the host for easy updates
- **Health Checks**: Built-in health monitoring for reliable orchestration

## Testing

The client automatically runs a smoke test that:
1. Pings the server
2. Lists available tools
3. Tests both corpus answer and text profile tools
4. Displays results for verification

##  Customization

### Adding New Documents

Place `.txt` files in `server/data/corpus/` - they'll be automatically indexed and searchable.

### Extending Tools

Add new tools in `server/tools/` and register them in `server/app.py` using the `@mcp.tool` decorator.

### Modifying Schemas

Update `server/schemas.py` to change response formats or add new data models.

## Learn More

- [Model Context Protocol (MCP)](https://modelcontextprotocol.io/)
- [FastMCP Framework](https://github.com/fastmcp/fastmcp)
- [Scikit-learn Text Processing](https://scikit-learn.org/stable/modules/feature_extraction.html#text-feature-extraction)

