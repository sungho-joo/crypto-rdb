SHELL := /bin/bash

STAGED := $(shell git diff --cached --name-only --diff-filter=ACMR -- 'src/***.py' | sed 's| |\\ |g')

all: format lint
	echo 'Makefile for crypto-rdb project'

format:
	black .
	isort .

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

init-dev:
	make init
	pip install -r requirements-dev.txt

init:
	pip install -U pip
	pip install -e .
	pip install -r requirements.txt
	bash ./hooks/install.sh

run-server:
	PYTHONPATH=src/ uvicorn src.main:app --host=0.0.0.0 --port 8085 --reload
