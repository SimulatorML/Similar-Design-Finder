.PHONY: build up down restart

DOCKER_COMPOSE_FILE=docker/docker-compose.yaml

build:
	docker compose -f $(DOCKER_COMPOSE_FILE) build

up:
	docker compose -f $(DOCKER_COMPOSE_FILE) up -d

down:
	docker compose -f $(DOCKER_COMPOSE_FILE) down

restart:
	docker compose -f $(DOCKER_COMPOSE_FILE) down
	docker compose -f $(DOCKER_COMPOSE_FILE) up -d
