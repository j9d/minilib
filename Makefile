lint:
	uv run black . && uv run isort .

build:
	docker compose build

up:
	docker compose up

shell:
	docker exec -it minilib /bin/bash
