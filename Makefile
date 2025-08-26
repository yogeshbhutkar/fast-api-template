.PHONY: build start down

build:
	docker compose build

start:
	docker compose up

down:
	docker compose down