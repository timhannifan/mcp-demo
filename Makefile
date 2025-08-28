SHELL := /bin/bash

.PHONY: up dev down logs rebuild client server-sh client-sh clean

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
