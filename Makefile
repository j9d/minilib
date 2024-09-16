lint:
	uv run black minilib && uv run isort minilib

build:
	docker compose build

up:
	docker compose up
