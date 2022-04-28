SERVICE_NAME:=contact_manager

.PHONY:env
env:
	pipenv shell

.PHONY:deps
deps:
	pipenv install

.PHONY:dev-server
dev-server:
	cd Capabilities; chalice local

.PHONY:dev-front
dev-front:
	cd Website; open index.html

.PHONY:lint
lint:
	pipenv run autopep8 --in-place --recursive .
	pipenv run flake8 . --max-line-length=127