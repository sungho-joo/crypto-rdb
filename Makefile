format:
		black . --line-length 104
		isort .

lint:
		env PYTHONPATH=. pytest --pylint --flake8 --mypy

utest:
		env PYTHONPATH=. pytest test/unittest/ -s

setup:
		pip install -r requirements.txt
		pre-commit install