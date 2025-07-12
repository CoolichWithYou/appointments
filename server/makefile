.PHONY: lint test install

SRC=. tests

lint:
	@echo "Running isort..."
	isort $(SRC)

	@echo "Running black..."
	black $(SRC)

	@echo "Running flake8..."
	flake8 $(SRC)

test:
	@echo "Running tests with pytest..."
	pytest --cache-clear -n 1

install:
	pip install -r requirements.txt
