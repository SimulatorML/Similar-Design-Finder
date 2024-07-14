.PHONY: build up down restart populate_db

DOCKER_COMPOSE_FILE=docker/docker-compose.yaml

build:
	docker compose -f $(DOCKER_COMPOSE_FILE) build

up:
	ENV=prod docker compose -f $(DOCKER_COMPOSE_FILE) up -d

down:
	docker compose -f $(DOCKER_COMPOSE_FILE) down

restart:
	docker compose -f $(DOCKER_COMPOSE_FILE) down
	ENV=prod docker compose -f $(DOCKER_COMPOSE_FILE) up -d

populate_db:
	poetry run python -m src.database.populate_db
