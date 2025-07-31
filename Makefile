.PHONY: install-local uninstall format run load-data create-tables drop-tables setup-local

SHELL := /bin/bash

requirements.txt: requirements.in
	pip-compile requirements.in

install: requirements.txt
	pip install -r requirements.txt

uninstall:
	pip freeze | xargs pip uninstall -y

format:
	black .
	isort .

run:
	source setenv.sh && fastapi run app/main.py --reload

load-data:
	source setenv.sh && python managedb.py load-data

create-tables:
	source setenv.sh && python managedb.py create-tables

drop-tables:
	source setenv.sh && python managedb.py drop-tables


setup-local: install format
	
