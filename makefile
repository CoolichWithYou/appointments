.PHONY: lint test install

SRC=server tests

lint:
	@echo "Running isort..."
	isort $(SRC)

	@echo "Running black..."
	black $(SRC)

	@echo "Running flake8..."
	flake8 $(SRC)

test:
	@echo "Running tests with pytest..."
	pytest

install:
	pip install -r server/requirements.txt
