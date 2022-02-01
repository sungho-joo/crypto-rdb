format:
		black . --line-length 104
		isort .

lint:
		env PYTHONPATH=. pytest --pylint --flake8 --mypy --ignore=src/wandb --ignore=test

utest:
		env PYTHONPATH=. pytest test/unittest/ -s

setup:
		pip install -r requirements.txt
		pip install -r requirements-dev.txt
		pre-commit install