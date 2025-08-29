SHELL := /bin/bash

.PHONY: up dev down logs rebuild client server-sh client-sh clean setup ollama ollama-shell

up:           ## build & run (internal network only)
	docker compose up --build

dev:          ## expose server at localhost:8765
	COMPOSE_PROFILES=dev docker compose up --build

down:         ## stop containers
	docker compose down

logs:         ## follow logs
	docker compose logs -f mcp-server mcp-client

rebuild:      ## rebuild images no cache
	docker compose build --no-cache

client:       ## run client only
	docker compose run --rm mcp-client

server-sh:    ## shell into server
	docker compose exec mcp-server bash

client-sh:    ## shell into client
	docker compose exec mcp-client bash

clean:        ## remove containers & volumes
	docker compose down -v

setup:        ## setup environment files from examples
	@if [ -f client/.env.example ]; then \
		if [ ! -f client/.env ]; then \
			cp client/.env.example client/.env; \
			echo "✅ Created client/.env from client/.env.example"; \
		else \
			echo "⚠️  client/.env already exists, skipping"; \
		fi; \
	else \
		echo "❌ client/.env.example not found"; \
	fi
	@if [ -f server/.env.example ]; then \
		if [ ! -f server/.env ]; then \
			cp server/.env.example server/.env; \
			echo "✅ Created server/.env from server/.env.example"; \
		else \
			echo "⚠️  server/.env already exists, skipping"; \
		fi; \
	else \
		echo "❌ server/.env.example not found"; \
	fi
	@echo " Setup complete!"

ollama:       ## start ollama services and pull default model
	COMPOSE_PROFILES=ollama docker compose up -d mcp-server ollama ollmcp
	@echo "🚀 Services started!"
	@echo "⏳ Waiting for Ollama to be ready..."
	@sleep 10
	@echo " Checking if llama3.2:1b model exists..."
	@if docker compose exec ollama ollama list | grep -q "llama3.2:1b"; then \
		echo "✅ Model already exists, skipping download"; \
	else \
		echo " Pulling llama3.2:1b model..."; \
		docker compose exec ollama ollama pull llama3.2:1b; \
	fi
	@echo "🎉 Ready to use OllMCP!"
	@echo "📝 To start OllMCP interactively, run:"
	@echo "   docker compose exec ollmcp bash"
	@echo "   ollmcp --mcp-server-url http://mcp-server:8765/mcp --host http://ollama:11434 --model llama3.2:1b"

ollama-shell: ## start ollama services and drop into shell
	COMPOSE_PROFILES=ollama docker compose up -d mcp-server ollama ollmcp
	@echo "🚀 Services started! Dropping into OllMCP container..."
	docker compose exec ollmcp bash
