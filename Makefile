.PHONY: migrate build up down

build:
	docker compose build

up:
	docker compose up -d

down:
	docker compose down

migrate:
	docker compose run web python schoolmind/manage.py migrate
