PYTHON=python3
VENV=venv
PIP=$(VENV)/bin/pip
PY=$(VENV)/bin/python

.PHONY: install test run server client clean freeze

install:
	$(PYTHON) -m venv $(VENV)
	$(PIP) install --upgrade pip
	if [ -f requirements.txt ]; then $(PIP) install -r requirements.txt; fi

test:
	if [ -x "$(PY)" ]; then $(PY) -m unittest discover -s tests -v; else $(PYTHON) -m unittest discover -s tests -v; fi

run:
	$(PYTHON) -m src.main

server:
	$(PYTHON) -m src.main

client:
	@echo "Cliente pendiente de la iteracion 2"

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

freeze:
	$(PIP) freeze > requirements.txt
