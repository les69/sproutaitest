.PHONY: tests

install:
	python -m pip install --upgrade pip wheel setuptools poetry==1.1.13
	poetry config virtualenvs.create false
	poetry install --no-dev --no-root

install-dev:
	python -m pip install --upgrade pip wheel setuptools poetry==1.1.13
	poetry config virtualenvs.create false
	poetry install --no-root

check-style:
	flake8  .

format:
	isort . --check --diff

full-test-suite:
	make check-style && make format && make django-tests

django-tests:
	cd ./sproutaitest && \
	python manage.py makemigrations && python manage.py migrate && \
	python manage.py test

cleanup-backlog:
	export PATH=/usr/local/bin && cd ./sproutaitest && python manage.py clear_backlog

run-django-server:
	cron && \
	cd ./sproutaitest && \
	python manage.py migrate && \
	python manage.py runserver 0.0.0.0:5000

run-mlapi-endpoint:
	docker build -t mlendpoint -f mlapi.Dockerfile . && \
	docker run -p 5001:5001 --network=endpointnetwork --name mlendpoint mlendpoint

run-ingestion-endpoint:
	docker build -t ingestion-endpoint -f ingestion.Dockerfile --target main . && \
	docker run -d -p 5000:5000 --network=endpointnetwork ingestion-endpoint

run-unit-tests:
	docker build -t ingestion-testing -f ingestion.Dockerfile --target test . && \
	docker run --rm -d ingestion-testing

start-network:
	docker network create -d bridge endpointnetwork