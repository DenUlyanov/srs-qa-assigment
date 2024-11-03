# Makefile
ENV = .venv

# Initialize the virtual environment and install pip-tools
init:
	python3 -m venv $(ENV)
	$(ENV)/bin/pip install virtualenv pip-tools

# Compile dependencies from pyproject.toml to requirements.txt
compile:
	$(ENV)/bin/pip-compile pyproject.toml --output-file requirements.txt

# Compile and upgrade dependencies
compile-upgrade:
	$(ENV)/bin/pip-compile pyproject.toml --upgrade --output-file requirements.txt

# Sync  dependencies from requirements.txt
sync:
	$(ENV)/bin/pip-sync requirements.txt

format:
	$(ENV)/bin/black .

lint:
	$(ENV)/bin/ruff .

type-check:
	$(ENV)/bin/mypy .

check: format lint type-check

# Run tests with pytest
test:
	$(ENV)/bin/pytest tests/

# Clean up generated requirements files
clean:
	rm -f requirements.txt
