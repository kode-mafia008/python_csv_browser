# Quick Start Guide

Get the CSV Browser up and running in 2 minutes!

## Prerequisites

- Docker Desktop installed ([Download here](https://www.docker.com/products/docker-desktop))
- 5GB free disk space
- Ports 3000, 8000, 5432, 6379 available

## Method 1: Using Start Script (Easiest)

```bash
# Make script executable (first time only)
chmod +x start.sh

# Run the application
./start.sh
```

Choose option 1 (Development) or 2 (Production) and you're done!

## Method 2: Using Make Commands

```bash
# Development mode (with hot-reload)
make dev

# Or production mode
make prod
```

## Method 3: Using Docker Compose Directly

```bash
# Development
docker-compose -f docker-compose.dev.yml up --build

# Production
docker-compose -f docker-compose.prod.yml up --build -d
```

## Access the Application

### Development Mode
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs

### Production Mode
- **Application**: http://localhost
- Backend is proxied through Nginx

## Default Login

- **Username**: `admin`
- **Password**: `admin123`

⚠️ Change this password immediately!

## First Steps

1. **Login** with admin credentials
2. **Upload a CSV file** (use the included `sample_data.csv`)
3. **View the file** in the table
4. **Open another browser tab** and see real-time updates!
5. **Create a regular user** by signing up
6. **Test different permissions** between admin and user roles

## Stopping the Application

```bash
# Using script
./stop.sh

# Using make
make down

# Using docker-compose
docker-compose -f docker-compose.dev.yml down
```

## Viewing Logs

```bash
# All services
make logs

# Backend only
make logs-backend

# Frontend only
make logs-frontend

# Using docker-compose
docker-compose -f docker-compose.dev.yml logs -f
```

## Troubleshooting

### Port Already in Use

```bash
# Check what's using the port
lsof -i :3000
lsof -i :8000

# Kill the process or change ports in docker-compose.yml
```

### Services Won't Start

```bash
# View logs to see the error
make logs

# Try cleaning everything and starting fresh
make clean
make dev
```

### Database Connection Error

```bash
# The backend waits for PostgreSQL to be ready
# If it still fails, try:
docker-compose -f docker-compose.dev.yml restart backend
```

### Reset Everything

```bash
# Stop and remove all data
make clean

# Start fresh
make dev
```

## Next Steps

- Read [README.md](README.md) for detailed information
- Check [DOCKER.md](DOCKER.md) for Docker specifics
- Review [SETUP.md](SETUP.md) for manual installation

## Common Tasks

### Create a New Admin User

```bash
# Access backend container
docker exec -it csv_browser_backend bash

# Run Python shell
python

# Create admin user
from app.core.database import SessionLocal
from app.services.user_service import UserService
from app.models.user import UserRole

db = SessionLocal()
UserService.create_user(db, "newadmin", "password123", UserRole.ADMIN)
db.close()
exit()
```

### Access Database

```bash
# PostgreSQL shell
make db-shell

# Then run SQL
\dt                    # List tables
SELECT * FROM users;   # View users
\q                     # Quit
```

### Access Redis

```bash
# Redis CLI
make redis-shell

# Then run commands
KEYS *                 # List all keys
GET some_key          # Get a value
```

### Backup Data

```bash
# Backup database
docker exec csv_browser_postgres pg_dump -U postgres csv_browser > backup.sql

# Backup uploads
tar -czf uploads_backup.tar.gz backend/uploads/
```

## Need Help?

- Check logs: `make logs`
- View container status: `docker ps`
- Restart services: `make restart`
- Full reset: `make clean && make dev`

---

**That's it!** You should now have a fully functional CSV Browser running locally.
