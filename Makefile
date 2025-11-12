.PHONY: help dev prod down clean logs build

help:
	@echo "CSV Browser - Docker Commands"
	@echo ""
	@echo "Development:"
	@echo "  make dev          - Start development environment with hot-reload"
	@echo "  make logs         - View logs from all containers"
	@echo "  make logs-backend - View backend logs"
	@echo "  make logs-frontend- View frontend logs"
	@echo ""
	@echo "Production:"
	@echo "  make prod         - Start production environment"
	@echo "  make build        - Build all Docker images"
	@echo ""
	@echo "Management:"
	@echo "  make down         - Stop all containers"
	@echo "  make clean        - Stop containers and remove volumes"
	@echo "  make restart      - Restart all containers"
	@echo "  make ps           - Show running containers"
	@echo ""
	@echo "Database:"
	@echo "  make db-shell     - Connect to PostgreSQL shell"
	@echo "  make redis-shell  - Connect to Redis shell"

dev:
	docker-compose -f docker-compose.dev.yml up --build

prod:
	docker-compose -f docker-compose.prod.yml up --build -d

down:
	docker-compose -f docker-compose.dev.yml down
	docker-compose -f docker-compose.prod.yml down

clean:
	docker-compose -f docker-compose.dev.yml down -v
	docker-compose -f docker-compose.prod.yml down -v
	rm -rf backend/uploads/*

logs:
	docker-compose -f docker-compose.dev.yml logs -f

logs-backend:
	docker-compose -f docker-compose.dev.yml logs -f backend

logs-frontend:
	docker-compose -f docker-compose.dev.yml logs -f frontend

build:
	docker-compose -f docker-compose.dev.yml build
	docker-compose -f docker-compose.prod.yml build

restart:
	docker-compose -f docker-compose.dev.yml restart

ps:
	docker-compose -f docker-compose.dev.yml ps

db-shell:
	docker exec -it csv_browser_postgres psql -U postgres -d csv_browser

redis-shell:
	docker exec -it csv_browser_redis redis-cli