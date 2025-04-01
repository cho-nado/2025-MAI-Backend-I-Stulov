.PHONY: migrate build up down

# Собрать Docker-образы
build:
	docker compose build

# Поднять сервисы в фоновом режиме
up:
	docker compose up -d

# Остановить и удалить сервисы
down:
	docker compose down

# Выполнить миграции (запускается в контейнере web)
migrate:
	docker compose run web python manage.py migrate
