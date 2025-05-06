.PHONY: migrate build up down createsuperuser createcustomsuperuser

build:
	docker compose build

up:
	docker compose up -d

down:
	docker compose down

migrate:
	docker compose run web python schoolmind/manage.py migrate

createsuperuser:
	docker compose run web python schoolmind/manage.py createsu

createcustomsuperuser:
	docker compose run web python schoolmind/manage.py createsuperuser

test:
	docker compose run web pytest schoolmind/core/tests/ -m "not selenium"

coverage:
	docker compose run web coverage run -m pytest schoolmind/core/tests/ -m "not selenium"
	docker compose run web coverage report
