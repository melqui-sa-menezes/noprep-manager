.ONESHELL:
PROJECT=noprep-manager
ROOT_DIR:=$(shell dirname $(realpath $(firstword $(MAKEFILE_LIST))))
POETRY := $(shell command -v poetry 2> /dev/null)
POETRY_VERSION := $(shell poetry --version 2> /dev/null | grep -oE '[0-9]+\.[0-9]+\.[0-9]+')
MAKEFLAGS += --no-print-directory

BLACK='\033[0;30m'
LIGHT_BLACK='\033[1;30m'
RED='\033[0;31m'
LIGHT_RED='\033[1;31m'
GREEN='\033[0;32m'
LIGHT_GREEN='\033[1;32m'
YELLOW='\033[0;33m'
LIGHT_YELLOW='\033[1;33m'
BLUE='\033[0;34m'
LIGHT_BLUE='\033[1;34m'
PURPLE='\033[0;35m'
LIGHT_PURPLE='\033[1;35m'
CYAN='\033[0;36m'
GRAY='\033[0;37m'
LIGHT_GRAY='\033[1;37m'
NC='\033[0m'

export PYTHONPATH=src
SRC_DIR := src

help:
	@echo ${LIGHT_BLUE}'Development shortcuts and commands'${NC}
	@echo ${LIGHT_GRAY}'For more information read the project Readme'${NC}
	@echo
	@echo ${LIGHT_YELLOW}'Usage:'${NC}
	@echo '  make '${LIGHT_GREEN}'<command>'${NC}
	@echo
	@echo ${LIGHT_YELLOW}'Commands:'${NC}
	@grep -E '^[a-zA-Z_-]+:.*?## ' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

install-poetry:
	@echo ${GRAY}'Checking if Poetry is installed...'${NC}
	@if [ -z "$(POETRY)" ]; then \
		echo ${LIGHT_YELLOW}'Poetry not found. Installing Poetry...'${NC}; \
		curl -sSL https://install.python-poetry.org | python3 -; \
		export POETRY=$(shell command -v poetry); \
		export POETRY_VERSION=$$($(POETRY) --version 2> /dev/null | grep -oE '[0-9]+\.[0-9]+\.[0-9]+'); \
		echo 'Poetry $(POETRY_VERSION) installed.' ${LIGHT_GREEN}'✓'${NC}; \
	else \
		echo 'Poetry $(POETRY_VERSION) is already installed' ${LIGHT_GREEN}'✓'${NC}; \
	fi

install: install-poetry ## Install dependencies
	@echo ${LIGHT_YELLOW}'Installing dependencies...'${NC}
	@$(POETRY) install -v --all-extras --sync

init: export POETRY_VIRTUALENVS_IN_PROJECT=true
init: export POETRY_VIRTUALENVS_PREFER_ACTIVE_PYTHON=true
init: ## Initialize the project
	@cp .env-example .env
	@$(MAKE) install
	@$(POETRY) env info
	@echo ${LIGHT_YELLOW}'Project initialized.'${NC}
	@echo ${LIGHT_YELLOW}'Please fill the .env file with the necessary environment variables.'${NC}

runserver: start-db migrate ## Start Database, apply migrations and run Django Server
	@echo ${LIGHT_YELLOW}'Running Django Server...'${NC}
	@export SIMPLE_SETTINGS=project.core.settings
	@$(POETRY) run python $(SRC_DIR)/manage.py runserver

run: runserver ## Run Django Server

migrate: ## Run Django migrations
	@echo ${LIGHT_YELLOW}'Running Django migrations...'${NC}
	@$(POETRY) run python $(SRC_DIR)/manage.py migrate
	@$(MAKE) erd
	@$(MAKE) show-migrations

migrations: ## Create Django migrations
	@echo ${LIGHT_YELLOW}'Creating Django migrations...'${NC}
	@$(POETRY) run python $(SRC_DIR)/manage.py makemigrations
	@$(MAKE) show-migrations

migration-initial: ## Create initial Django migration. Example: make migration-initial app=drivers
	@if [ $(app) ]; then \
		echo ${LIGHT_YELLOW}'Creating initial Django migration for app $(app)...'${NC}; \
		$(POETRY) run python $(SRC_DIR)/manage.py makemigrations $(app); \
	else \
		echo ${LIGHT_YELLOW}'Please provide an app name. Usage: make migration-initial app=<app_name>'${NC}; exit 1; \
	fi

show-migrations: ## Show Django migrations
	@echo ${LIGHT_YELLOW}'Showing Django migrations...'${NC}
	@$(POETRY) run python $(SRC_DIR)/manage.py showmigrations

populate-db: ## Populate the database with initial data
	@echo ${LIGHT_YELLOW}'Populating the database with initial data...'${NC}
	@$(POETRY) run python $(SRC_DIR)/manage.py loaddata initial_data.json

start-db: ## Start the database
	@echo ${LIGHT_YELLOW}'Starting the database...'${NC}
	@docker compose up -d postgres

create-db: start-db ## Create the database
	@echo ${LIGHT_YELLOW}'Starting database services...'${NC}
	@$(MAKE) migrations
	@$(MAKE) migrate
	@$(MAKE) create-superuser
	@$(MAKE) populate-db
	@echo ${LIGHT_YELLOW}'Database setup completed.'${NC}

recreate-db: ## Recreate the database
	@echo ${LIGHT_YELLOW}'Recreating the database...'${NC}
	@docker compose down -v
	@$(MAKE) create-db

create-superuser: migrate ## Create Django superuser
	@echo ${LIGHT_YELLOW}'Creating Django superuser...'${NC}
	@export DJANGO_SUPERUSER_PASSWORD=admin
	@$(POETRY) run python $(SRC_DIR)/manage.py createsuperuser --username admin --email 'admin@example.com' --noinput
	@echo ${LIGHT_YELLOW}'Superuser created with username "admin" and password "admin".'${NC}

lint: ## Run linters
	@echo ${LIGHT_YELLOW}'Running linters...'${NC}
	@echo ${LIGHT_YELLOW}'Step 1: black'${NC}
	@$(POETRY) run black --check --config=pyproject.toml $(SRC_DIR)
	@echo ${LIGHT_YELLOW}'Step 2: ruff'${NC}
	@$(POETRY) run ruff check $(SRC_DIR)

lint-fix: ## Fix linters
	@echo ${LIGHT_YELLOW}'Fixing linters...'${NC}
	@echo ${LIGHT_YELLOW}'Step 1: black'${NC}
	@$(POETRY) run black --config=pyproject.toml $(SRC_DIR)
	@echo ${LIGHT_YELLOW}'Step 2: ruff'${NC}
	@$(POETRY) run ruff check $(SRC_DIR) --fix
	@$(MAKE) lint

erd: ## Generate ERD
	@echo ${LIGHT_YELLOW}'Generating ERD...'${NC}
	@$(POETRY) run python $(SRC_DIR)/manage.py graph_models -a -o erd.png

test: ## Run tests
	@echo ${LIGHT_YELLOW}'Running tests...'${NC}
	@$(POETRY) run pytest

coverage: ## Run tests with coverage
	@echo ${LIGHT_YELLOW}'Running tests with coverage...'${NC}
	@$(POETRY) run pytest --cov

