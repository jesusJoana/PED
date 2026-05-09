PYTHON=python3
VENV=venv
PIP=$(VENV)/bin/pip
PY=$(VENV)/bin/python
FILE?=$(CURDIR)/fichero.txt
HOST?=127.0.0.1
PORT?=5005

.PHONY: install test run server client clean freeze

install:
	$(PYTHON) -m venv $(VENV)
	$(PIP) install --upgrade pip
	if [ -f requirements.txt ]; then $(PIP) install -r requirements.txt; fi

test:
	$(PY) -m unittest discover -s tests -v

run:
	./cli5 $(FILE) --host $(HOST) --port $(PORT)

server:
	./serv5 --host $(HOST) --port $(PORT)

client:
	./cli5 $(FILE) --host $(HOST) --port $(PORT)

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

freeze:
	$(PIP) freeze > requirements.txt
