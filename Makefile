# Makefile
ENV = .venv

# Set the PATH so that the virtual environment is used automatically
export PATH := $(ENV)/bin:$(PATH)

# Initialize the virtual environment and install pip-tools
init:
	python3 -m venv $(ENV)
	pip install virtualenv pip-tools

# Compile dependencies from pyproject.toml to requirements.txt
compile:
	pip-compile pyproject.toml --output-file requirements.txt

# Compile and upgrade dependencies
compile-upgrade:
	pip-compile pyproject.toml --upgrade --output-file requirements.txt

# Sync dependencies from requirements.txt
sync:
	pip-sync requirements.txt

format:
	black .

lint:
	ruff check --fix

type-check:
	mypy .

check: format lint type-check

# Run tests with pytest
test:
	pytest tests/ -n auto --html=reports/ui_test_report.html --self-contained-html

# Clean up generated requirements files
clean:
	rm -f requirements.txt
