dev:
	uvicorn backend.app.main:app --reload --port 8000

test:
	pytest backend/app/tests/ -v

migrate:
	alembic upgrade head

lint:
	pre-commit run --all-files

up:
	docker-compose up -d

down:
	docker-compose down