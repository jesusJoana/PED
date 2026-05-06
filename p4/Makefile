PYTHON=python3
VENV=venv
PIP=$(VENV)/bin/pip
PY=$(VENV)/bin/python
FILE?=prueba.txt

.PHONY: install test run clean freeze

install:
	$(PYTHON) -m venv $(VENV)
	$(PIP) install --upgrade pip
	if [ -f requirements.txt ]; then $(PIP) install -r requirements.txt; fi

test:
	$(PY) -m unittest discover -s tests -v

run:
	$(PY) src/main.py $(FILE)

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

freeze:
	$(PIP) freeze > requirements.txt