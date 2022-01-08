REQ=dev

install:
	pip install -r requirements/$(REQ).txt

check:
	flake8 src
	isort -c src
	# mypy

deploy:
	@./deploy.sh
