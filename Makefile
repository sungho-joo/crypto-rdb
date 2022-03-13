format:
		black . --line-length 104
		isort .

lint:
		env PYTHONPATH=. pytest --pylint --flake8 

utest:
		env PYTHONPATH=. pytest test/unittest/ -s

setup:
		pip install -r requirements.txt
		pip install -r requirements-dev.txt
		pre-commit install

run_server:
	PYTHONPATH=src/ uvicorn src.main:app --host=0.0.0.0 --port 8085 --reload
