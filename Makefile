.ONESHELL:
PROJECT=noprep-manager
ROOT_DIR:=$(shell dirname $(realpath $(firstword $(MAKEFILE_LIST))))
POETRY := $(shell command -v poetry --directory=$(ROOT_DIR) 2> /dev/null)
POETRY_VERSION := $(shell poetry --version 2> /dev/null | cut -d '' -f 3)
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

help:
	@echo ${LIGHT_BLUE}'Development shortcuts and commands'${NC}
	@echo ${LIGHT_GRAY}'For more information read the project Readme'${NC}
	@echo
	@echo ${LIGHT_YELLOW}'Usage:'${NC}
	@echo '  make '${LIGHT_GREEN}'<command>'${NC}
	@echo
	@echo ${LIGHT_YELLOW}'Commands:'${NC}
	@fgrep -h "##" $(MAKEFILE_LIST) | fgrep -v fgrep | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

install-poetry:
	@echo ${GRAY}'Checking if Poetry is installed...'${NC}
	@@if [ -z "$(POETRY)" ]; then \
		echo ${LIGHT_YELLOW}'Poetry not found. Installing Poetry...'${NC}; \
		curl -sSL https://install.python-poetry.org | python3 -; \
		echo '$(POETRY_VERSION) installed.' ${LIGHT_GREEN}'✓'${NC}; \
	else \
		echo '$(POETRY_VERSION) is already installed' ${LIGHT_GREEN}'✓'${NC}; \
	fi

install: ## Install dependencies
	@echo ${LIGHT_YELLOW}'Installing dependencies...'${NC}
	@$(POETRY) install -v --all-extras --sync

init: export POETRY_VIRTUALENVS_IN_PROJECT=true
init: export POETRY_VIRTUALENVS_PREFER_ACTIVE_PYTHON=true
init: ## Initialize the project
	@cp .env-example .env
	@$(MAKE) install-poetry
	@$(MAKE) install
	@$(POETRY) env info
	@echo ${LIGHT_YELLOW}'Project initialized.'${NC}
	@echo ${LIGHT_YELLOW}'Please fill the .env file with the necessary environment variables.'${NC}

runserver: start-db migrate ## Start Database, apply migrations and run Django Admin
	@echo ${LIGHT_YELLOW}'Running Django Admin...'${NC}
	@export SIMPLE_SETTINGS=project.core.settings
	@$(POETRY) run python src/manage.py runserver

run: start-db ## Run Django Admin
	@echo ${LIGHT_YELLOW}'Running Django Admin...'${NC}
	@export SIMPLE_SETTINGS=project.core.settings
	@$(POETRY) run python src/manage.py runserver

migrate: ## Run Django migrations
	@echo ${LIGHT_YELLOW}'Running Django migrations...'${NC}
	@$(POETRY) run python src/manage.py migrate
	@$(MAKE) show-migrations

migrations: ## Create Django migrations
	@echo ${LIGHT_YELLOW}'Creating Django migrations...'${NC}
	@$(POETRY) run python src/manage.py makemigrations
	@$(MAKE) show-migrations

migration-initial: ## Create initial Django migration. Example: make migration-initial app=drivers
	@if [ $(app) ]; then
		@echo ${LIGHT_YELLOW}'Creating initial Django migration for app $(app)...'${NC}
		@$(POETRY) run python src/manage.py makemigrations $(app)
	else
	@echo ${LIGHT_YELLOW}'Please provide an app name.'${NC}; exit 1;\
	fi

show-migrations: ## Show Django migrations
	@echo ${LIGHT_YELLOW}'Showing Django migrations...'${NC}
	@$(POETRY) run python src/manage.py showmigrations drivers events

populate-db: export DJANGO_SUPERUSER_PASSWORD=admin
populate-db: ## Populate the database with initial data
	@echo ${LIGHT_YELLOW}'Creating Django superuser...'${NC}
	@$(POETRY) run python src/manage.py createsuperuser --username admin --email 'admin@econome.com.br' --noinput
	@echo ${LIGHT_YELLOW}'Populating the database with initial data...'${NC}
	@$(POETRY) run python src/manage.py syncdata initial_data.json --skip-remove

start-db: ## Start the database
	@echo ${LIGHT_YELLOW}'Starting the database...'${NC}
	@docker compose up -d postgres

create-db: ## Create the database
	@echo ${LIGHT_YELLOW}'Creating the database...'${NC}
	@docker compose up -d
	@echo ${LIGHT_YELLOW}'Database recreated.'${NC}
	@$(MAKE) migrations
	@echo ${LIGHT_YELLOW}'Migrations created.'${NC}
	@$(MAKE) migrate
	@echo ${LIGHT_YELLOW}'Migrations applied.'${NC}
	@$(MAKE) populate-db
	@echo ${LIGHT_YELLOW}'Database populated.'${NC}


recreate-db: ## Recreate the database
	@echo ${LIGHT_YELLOW}'Recreating the database...'${NC}
	@docker compose down -v
	@$(MAKE) create-db

create-superuser: migrate ## Create Django superuser
	@echo ${LIGHT_YELLOW}'Creating Django superuser...'${NC}
	@$(POETRY) run python src/manage.py createsuperuser --username admin --email 'admin@econome.com.br' --noinput || true
	@echo "from django.contrib.auth import get_user_model; User = get_user_model(); user = User.objects.get(username='admin'); user.set_password('$(pass)'); user.save()" | $(POETRY) run python src/manage.py shell
	@echo ${LIGHT_YELLOW}'Superuser created with username "admin" and the specified password.'${NC}

lint: ## Run linters
	@echo ${LIGHT_YELLOW}'Running linters...'${NC}
	@echo ${LIGHT_YELLOW}'step 1: black'${NC}
	@$(POETRY) run black --check --config=pyproject.toml src
	@echo ${LIGHT_YELLOW}'step 2: ruff'${NC}
	@$(POETRY) run ruff check src


lint-fix: ## Fix linters
	@echo ${LIGHT_YELLOW}'Fixing linters...'${NC}
	@echo ${LIGHT_YELLOW}'step 1: black'${NC}
	@$(POETRY) run black --config=./pyproject.toml src
	@echo ${LIGHT_YELLOW}'step 2: ruff'${NC}
	@$(POETRY) run ruff check src --fix
	@$(MAKE) lint

