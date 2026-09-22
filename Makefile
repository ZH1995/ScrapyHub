.PHONY: install db-up db-down run test lint

install:
	python -m pip install -r requirements.txt

db-up:
	docker compose up -d

db-down:
	docker compose down

run:
	python run_all.py

test:
	python -m pytest -q

lint:
	python -m compileall scrapyhub tests run.py run_all.py
