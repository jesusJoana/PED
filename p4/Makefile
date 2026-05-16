PYTHON=python3
VENV=venv
PIP=$(VENV)/bin/pip
PY=$(VENV)/bin/python
FILE?=$(CURDIR)/fichero.txt
SOCKET?=/tmp/serv4.sock

.PHONY: install test run server client clean freeze

install:
	$(PYTHON) -m venv $(VENV)
	$(PIP) install --upgrade pip
	if [ -f requirements.txt ]; then $(PIP) install -r requirements.txt; fi

test:
	$(PY) -m unittest discover -s tests -v

run:
	./cli4 $(FILE) --socket $(SOCKET)

server:
	./serv4 --socket $(SOCKET)

client:
	./cli4 $(FILE) --socket $(SOCKET)

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

freeze:
	$(PIP) freeze > requirements.txt
