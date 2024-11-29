.PHONY: dev-build
dev-build:
	docker compose -f compose-dev.yml build

.PHONY: dev-up-d
dev-up-d:
	docker compose -f compose-dev.yml up -d

.PHONY: dev
dev:
	@make dev-build
	@make dev-up-d

.PHONY: down
down:
	docker compose -f compose-dev.yml down

.PHONY: bash
bash:
	docker compose -f compose-dev.yml exec discord-bot bash

.PHONY: logs
logs:
	docker compose -f compose-dev.yml logs

# Lintとフォーマット
.PHONY: black
black:
	docker compose -f compose-dev.yml exec discord-bot black .

.PHONY: isort
isort:
	docker compose -f compose-dev.yml exec discord-bot isort .

.PHONY: flake8
flake8:
	docker compose -f compose-dev.yml exec discord-bot flake8 .

.PHONY: lint
lint:
	@make black
	@make isort
	@make flake8
