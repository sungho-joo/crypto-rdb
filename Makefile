STAGED := $(shell git diff --cached --name-only --diff-filter=ACMR -- 'src/***.py' | sed 's| |\\ |g')

all: format lint
	echo 'Makefile for crypto-rdb project'

format:
	black .
	isort .
	nbqa black .
	nbqa isort .

lint:
	pytest src/ --pylint --flake8 --mypy

lint-all:
	pytest src/ --pylint --flake8 --mypy --cache-clear

lint-staged:
ifdef STAGED
	pytest $(STAGED) --pylint --flake8 --cache-clear
	# nbqa pytest $(STAGED) --pylint --flake8 --cache-clear
else
	@echo "No Staged Python File in the src folder"
endif

init:
	pip install -U pip
	pip install -e .
	pip install -r requirements.txt
	jupyter contrib nbextension install --user
	jupyter nbextensions_configurator enable --user
	python3 -m ipykernel install --user

init-dev:
	make init
	pip install -r requirements-dev.txt
	bash ./scripts/install.sh

server:
	docker-compose up -d

server-clean:
	docker-compose down -v
