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

setup-local: install-local format
	
