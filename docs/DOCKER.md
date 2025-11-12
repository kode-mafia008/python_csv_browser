# Docker Setup Guide

This guide explains how to run the CSV Browser application using Docker.

## Prerequisites

- Docker Engine 20.10+
- Docker Compose 2.0+

## Quick Start

### Development Mode (with hot-reload)

```bash
# Start all services
make dev

# Or using docker-compose directly
docker-compose -f docker-compose.dev.yml up --build
```

The application will be available at:
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs

### Production Mode

```bash
# Start all services in production mode
make prod

# Or using docker-compose directly
docker-compose -f docker-compose.prod.yml up --build -d
```

The application will be available at:
- Frontend: http://localhost (port 80)
- Backend is accessed through nginx proxy

## Docker Services

The application consists of 4 services:

1. **postgres** - PostgreSQL 15 database
2. **redis** - Redis 7 cache (for future session/caching features)
3. **backend** - FastAPI application
4. **frontend** - React application (dev: Vite server, prod: Nginx)

## Architecture

```
┌─────────────────────────────────────────────────┐
│                   Frontend                       │
│         (React + Vite/Nginx)                    │
│                Port: 3000/80                     │
└──────────────────┬──────────────────────────────┘
                   │
                   │ HTTP/WebSocket
                   ▼
┌─────────────────────────────────────────────────┐
│                  Backend                         │
│              (FastAPI)                           │
│                Port: 8000                        │
└────────┬─────────────────────┬──────────────────┘
         │                     │
         │                     │
         ▼                     ▼
┌────────────────┐    ┌────────────────┐
│   PostgreSQL   │    │     Redis      │
│   Port: 5432   │    │   Port: 6379   │
└────────────────┘    └────────────────┘
```

## Environment Variables

The application uses `.env.docker` for Docker configuration:

```env
DATABASE_URL=postgresql://postgres:postgres@postgres:5432/csv_browser
REDIS_URL=redis://redis:6379
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
UPLOAD_DIR=./uploads
```

### Important Notes:
- Service names (postgres, redis) are used as hostnames in Docker network
- In production, change the `SECRET_KEY` to a secure random string
- PostgreSQL and Redis data persist in Docker volumes

## Makefile Commands

### Development
```bash
make dev              # Start development environment
make logs             # View all logs
make logs-backend     # View backend logs only
make logs-frontend    # View frontend logs only
```

### Production
```bash
make prod             # Start production environment
make build            # Build Docker images
```

### Management
```bash
make down             # Stop all containers
make clean            # Stop and remove volumes (⚠️ deletes data)
make restart          # Restart containers
make ps               # Show running containers
```

### Database Access
```bash
make db-shell         # PostgreSQL shell
make redis-shell      # Redis CLI
```

## Development Workflow

### 1. Start Development Environment

```bash
make dev
```

This will:
- Build all Docker images
- Start PostgreSQL and Redis
- Initialize database with admin user
- Start backend with hot-reload
- Start frontend with Vite dev server

### 2. Code Changes

**Backend**: Changes in `backend/app/` are automatically reloaded
**Frontend**: Changes in `frontend/src/` are automatically reloaded

### 3. View Logs

```bash
# All services
make logs

# Specific service
docker-compose -f docker-compose.dev.yml logs -f backend
docker-compose -f docker-compose.dev.yml logs -f frontend
```

### 4. Database Access

```bash
# PostgreSQL
make db-shell
# Then run SQL commands:
# \dt              - List tables
# SELECT * FROM users;

# Redis
make redis-shell
# Then run Redis commands:
# KEYS *
# GET some_key
```

## Production Deployment

### 1. Build Images

```bash
make build
```

### 2. Configure Environment

Edit `.env.docker` with production values:
```env
SECRET_KEY=<generate-strong-random-key>
POSTGRES_PASSWORD=<secure-password>
```

### 3. Start Production Services

```bash
make prod
```

### 4. Verify Services

```bash
make ps
```

All services should show as "Up" and healthy.

## Volumes

Docker volumes persist data across container restarts:

- `postgres_data` - Database files
- `redis_data` - Redis persistence
- `./backend/uploads` - Uploaded CSV files (bind mount)

### Backup Data

```bash
# Backup PostgreSQL
docker exec csv_browser_postgres pg_dump -U postgres csv_browser > backup.sql

# Backup uploads
tar -czf uploads_backup.tar.gz backend/uploads/
```

### Restore Data

```bash
# Restore PostgreSQL
docker exec -i csv_browser_postgres psql -U postgres csv_browser < backup.sql

# Restore uploads
tar -xzf uploads_backup.tar.gz
```

## Troubleshooting

### Container won't start

```bash
# Check logs
docker-compose -f docker-compose.dev.yml logs

# Check specific service
docker logs csv_browser_backend
```

### Database connection error

```bash
# Verify PostgreSQL is running
docker ps | grep postgres

# Check PostgreSQL logs
docker logs csv_browser_postgres

# Test connection
make db-shell
```

### Port already in use

```bash
# Find process using port
lsof -i :8000
lsof -i :3000

# Change port in docker-compose file
# For example, change "3000:3000" to "3001:3000"
```

### Reset everything

```bash
# Stop all containers and remove volumes
make clean

# Remove all Docker images
docker-compose -f docker-compose.dev.yml down --rmi all

# Start fresh
make dev
```

### Frontend can't connect to backend

1. Check backend is running: `docker ps | grep backend`
2. Check backend logs: `make logs-backend`
3. Verify network: `docker network ls`
4. Test backend: `curl http://localhost:8000/health`

### Database initialization failed

```bash
# Manual initialization
docker exec -it csv_browser_backend python init_db.py
```

## Docker Compose Files

### docker-compose.dev.yml
- Development environment
- Hot-reload enabled
- Vite dev server for frontend
- Ports exposed for direct access

### docker-compose.prod.yml
- Production environment
- Optimized builds
- Nginx for frontend
- Health checks enabled
- Auto-restart on failure

## Performance Tips

### Development
- Use volume mounts for hot-reload
- Keep node_modules in container (faster)
- Use BuildKit for faster builds:
  ```bash
  export DOCKER_BUILDKIT=1
  ```

### Production
- Multi-stage builds reduce image size
- Nginx serves static files efficiently
- Use multiple uvicorn workers:
  ```yaml
  command: uvicorn app.main:app --workers 4
  ```

## Security Considerations

### Production Checklist
- [ ] Change SECRET_KEY to random value
- [ ] Change PostgreSQL password
- [ ] Enable HTTPS (use reverse proxy like Traefik)
- [ ] Don't expose database ports
- [ ] Use environment variables for secrets
- [ ] Enable Docker secrets for sensitive data
- [ ] Keep images updated
- [ ] Run containers as non-root user

### Example with Docker Secrets

```yaml
services:
  backend:
    secrets:
      - db_password
      - secret_key

secrets:
  db_password:
    file: ./secrets/db_password.txt
  secret_key:
    file: ./secrets/secret_key.txt
```

## Default Credentials

After initialization, admin account is created:
- **Username**: admin
- **Password**: admin123

⚠️ **Change this immediately in production!**

## Monitoring

### Container Stats
```bash
docker stats
```

### Resource Usage
```bash
docker-compose -f docker-compose.dev.yml ps
docker system df
```

### Clean Up Unused Resources
```bash
docker system prune -a
docker volume prune
```

## CI/CD Integration

### GitHub Actions Example

```yaml
name: Docker Build

on:
  push:
    branches: [main]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Build images
        run: docker-compose -f docker-compose.prod.yml build
      - name: Run tests
        run: docker-compose -f docker-compose.prod.yml run backend pytest
```

## Next Steps

- Set up HTTPS with Let's Encrypt
- Configure backup automation
- Set up monitoring (Prometheus/Grafana)
- Implement log aggregation (ELK stack)
- Add container orchestration (Kubernetes)
