SHELL := /bin/bash

requirements/requirements.txt: requirements/requirements.in
	pip-compile requirements/requirements.in

requirements/requirements-local.txt: requirements/requirements-local.in requirements/requirements.txt
	pip-compile requirements/requirements-local.in

install-local: requirements/requirements-local.txt
	pip install -r requirements/requirements-local.txt

uninstall:
	pip freeze | xargs pip uninstall -y

format:
	black .
	isort .

run:
	source setenv.sh
	fastapi run app/main.py --reload

load-data:
	source setenv.sh
	python app/db.py load ../link_info.parquet.gz ../duval_jan1_2024.parquet.gz

create-tables:
	source setenv.sh
	python app/db.py create

drop-tables:
	source setenv.sh
	python app/db.py drop


setup-local: install-local format
	
