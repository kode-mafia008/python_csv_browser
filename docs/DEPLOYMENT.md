# Deployment Guide

Complete guide for deploying CSV Browser in various environments.

## Table of Contents
1. [Local Development](#local-development)
2. [Production Docker](#production-docker)
3. [Cloud Deployment](#cloud-deployment)
4. [Security Hardening](#security-hardening)
5. [Monitoring & Logging](#monitoring--logging)

---

## Local Development

### Quick Start
```bash
./start.sh
# Select option 1 (Development)
```

### Manual Start
```bash
docker-compose -f docker-compose.dev.yml up --build
```

### What Gets Started
- PostgreSQL (port 5432)
- Redis (port 6379)
- Backend (port 8000) with hot-reload
- Frontend (port 3000) with Vite dev server

### Access Points
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs
- PostgreSQL: localhost:5432
- Redis: localhost:6379

---

## Production Docker

### 1. Prepare Environment

**Update `.env.docker`:**
```bash
# Generate a secure secret key
python -c "import secrets; print(secrets.token_urlsafe(32))"

# Edit .env.docker
DATABASE_URL=postgresql://postgres:SECURE_PASSWORD@postgres:5432/csv_browser
REDIS_URL=redis://redis:6379
SECRET_KEY=<generated-secret-key>
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
UPLOAD_DIR=./uploads

POSTGRES_USER=postgres
POSTGRES_PASSWORD=SECURE_PASSWORD
POSTGRES_DB=csv_browser
```

### 2. Build and Start

```bash
# Build images
make build

# Start in production mode
make prod

# Verify all services are running
docker ps
```

### 3. Create Admin User

```bash
# Admin user is auto-created with credentials:
# Username: admin
# Password: admin123

# Change the password immediately!
docker exec -it csv_browser_backend_prod python -c "
from app.core.database import SessionLocal
from app.core.security import get_password_hash
from app.models.user import User

db = SessionLocal()
admin = db.query(User).filter(User.username == 'admin').first()
admin.hashed_password = get_password_hash('NEW_SECURE_PASSWORD')
db.commit()
db.close()
"
```

### 4. Verify Deployment

```bash
# Check all services are healthy
docker-compose -f docker-compose.prod.yml ps

# Test the API
curl http://localhost/api/health

# View logs
docker-compose -f docker-compose.prod.yml logs
```

---

## Cloud Deployment

### AWS (EC2 + Docker)

**1. Launch EC2 Instance**
```bash
# Minimum: t3.medium (2 vCPU, 4GB RAM)
# Storage: 20GB+ SSD
# Security Group: Allow ports 80, 443, 22
```

**2. Install Docker**
```bash
# On Ubuntu 22.04
sudo apt update
sudo apt install -y docker.io docker-compose
sudo systemctl enable docker
sudo usermod -aG docker ubuntu
```

**3. Deploy Application**
```bash
# Clone or upload project
git clone <your-repo>
cd csv-browser

# Update environment variables
nano .env.docker

# Start services
make prod
```

**4. Set Up Nginx Reverse Proxy (on host)**
```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://localhost;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
    }
}
```

**5. SSL with Let's Encrypt**
```bash
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d your-domain.com
```

### Google Cloud Platform (Cloud Run)

**1. Build and Push Images**
```bash
# Backend
gcloud builds submit --tag gcr.io/PROJECT_ID/csv-browser-backend ./backend

# Frontend
gcloud builds submit --tag gcr.io/PROJECT_ID/csv-browser-frontend ./frontend
```

**2. Deploy Services**
```bash
# Deploy backend
gcloud run deploy csv-browser-backend \
  --image gcr.io/PROJECT_ID/csv-browser-backend \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated

# Deploy frontend
gcloud run deploy csv-browser-frontend \
  --image gcr.io/PROJECT_ID/csv-browser-frontend \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated
```

**3. Set Up Cloud SQL (PostgreSQL)**
```bash
gcloud sql instances create csv-browser-db \
  --database-version=POSTGRES_15 \
  --tier=db-f1-micro \
  --region=us-central1

# Update DATABASE_URL in Cloud Run environment
```

### DigitalOcean (App Platform)

**1. Create App**
- Connect GitHub repository
- Auto-detect Docker Compose
- Set environment variables
- Deploy

**2. Add Managed Database**
- Create PostgreSQL cluster
- Create Redis cluster
- Update connection strings

---

## Security Hardening

### 1. Environment Variables

**Never commit sensitive data!**
```bash
# Use Docker secrets in production
echo "SECURE_PASSWORD" | docker secret create db_password -
echo "SECRET_KEY" | docker secret create jwt_secret -
```

**Update docker-compose.prod.yml:**
```yaml
services:
  backend:
    secrets:
      - db_password
      - jwt_secret
    environment:
      DATABASE_URL: postgresql://postgres:${db_password}@postgres:5432/csv_browser
      SECRET_KEY_FILE: /run/secrets/jwt_secret

secrets:
  db_password:
    external: true
  jwt_secret:
    external: true
```

### 2. Network Security

**Isolate Services:**
```yaml
# docker-compose.prod.yml
services:
  postgres:
    # Remove ports exposure - only internal access
    # ports:
    #   - "5432:5432"

  redis:
    # Remove ports exposure
    # ports:
    #   - "6379:6379"
```

**Use Internal Network:**
```yaml
networks:
  frontend:
  backend:

services:
  frontend:
    networks:
      - frontend
      - backend

  backend:
    networks:
      - backend

  postgres:
    networks:
      - backend  # Only backend can access
```

### 3. CORS Configuration

**Update `backend/app/main.py`:**
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://your-domain.com"],  # Specific domain only
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)
```

### 4. Rate Limiting

**Add to backend:**
```bash
# requirements.txt
slowapi==0.1.9

# app/main.py
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# On routes
@app.post("/api/auth/login")
@limiter.limit("5/minute")
async def login(request: Request, ...):
    ...
```

### 5. HTTPS Only

**Nginx Configuration:**
```nginx
server {
    listen 80;
    server_name your-domain.com;
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name your-domain.com;

    ssl_certificate /etc/letsencrypt/live/your-domain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/your-domain.com/privkey.pem;

    # Strong SSL settings
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;
    ssl_prefer_server_ciphers on;

    location / {
        proxy_pass http://localhost;
    }
}
```

### 6. File Upload Security

**Limit file size in nginx:**
```nginx
client_max_body_size 10M;
```

**Validate file type in backend:**
```python
# backend/app/api/admin.py
ALLOWED_EXTENSIONS = {'.csv'}
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB

def validate_file(file):
    if not file.filename.endswith('.csv'):
        raise HTTPException(400, "Only CSV files allowed")

    # Check actual content type
    content = file.file.read(1024)
    file.file.seek(0)
    # Add CSV validation logic
```

---

## Monitoring & Logging

### 1. Health Checks

**Add to docker-compose.prod.yml:**
```yaml
services:
  backend:
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s
```

### 2. Logging

**Centralized logging:**
```yaml
services:
  backend:
    logging:
      driver: "json-file"
      options:
        max-size: "10m"
        max-file: "3"
```

**View logs:**
```bash
# All logs
docker-compose -f docker-compose.prod.yml logs -f

# Specific service
docker-compose -f docker-compose.prod.yml logs -f backend

# Export logs
docker-compose -f docker-compose.prod.yml logs > app.log
```

### 3. Prometheus Metrics

**Add to requirements.txt:**
```
prometheus-fastapi-instrumentator==6.1.0
```

**Update backend/app/main.py:**
```python
from prometheus_fastapi_instrumentator import Instrumentator

app = FastAPI()
Instrumentator().instrument(app).expose(app)
```

### 4. Backup Strategy

**Automated backups:**
```bash
#!/bin/bash
# backup.sh

DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="./backups"

# Backup database
docker exec csv_browser_postgres_prod pg_dump -U postgres csv_browser > "$BACKUP_DIR/db_$DATE.sql"

# Backup uploads
tar -czf "$BACKUP_DIR/uploads_$DATE.tar.gz" backend/uploads/

# Keep only last 7 days
find $BACKUP_DIR -type f -mtime +7 -delete
```

**Cron job:**
```bash
# Run daily at 2 AM
0 2 * * * /path/to/backup.sh
```

---

## Scaling

### Horizontal Scaling

**Docker Swarm:**
```bash
# Initialize swarm
docker swarm init

# Deploy stack
docker stack deploy -c docker-compose.prod.yml csv_browser

# Scale backend
docker service scale csv_browser_backend=3
```

**Kubernetes:**
```yaml
# kubernetes/deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: csv-browser-backend
spec:
  replicas: 3
  selector:
    matchLabels:
      app: backend
  template:
    spec:
      containers:
      - name: backend
        image: your-registry/csv-browser-backend
```

### Database Scaling

**PostgreSQL Read Replicas:**
```yaml
services:
  postgres-primary:
    image: postgres:15-alpine
    environment:
      POSTGRES_REPLICATION_MODE: master

  postgres-replica:
    image: postgres:15-alpine
    environment:
      POSTGRES_REPLICATION_MODE: slave
      POSTGRES_MASTER_SERVICE: postgres-primary
```

---

## Troubleshooting

### Service Won't Start
```bash
# Check logs
docker-compose logs service_name

# Verify configuration
docker-compose config

# Remove and rebuild
docker-compose down -v
docker-compose up --build
```

### Database Connection Issues
```bash
# Test connection
docker exec csv_browser_postgres psql -U postgres -c "SELECT 1"

# Check network
docker network inspect csv_browser_network
```

### Performance Issues
```bash
# Check resource usage
docker stats

# Increase resources in docker-compose
services:
  backend:
    deploy:
      resources:
        limits:
          cpus: '2'
          memory: 2G
```

---

## Rollback Procedure

```bash
# 1. Stop current version
docker-compose -f docker-compose.prod.yml down

# 2. Restore previous images
docker pull your-registry/csv-browser-backend:previous
docker pull your-registry/csv-browser-frontend:previous

# 3. Restore database
docker exec -i csv_browser_postgres psql -U postgres csv_browser < backup.sql

# 4. Start services
docker-compose -f docker-compose.prod.yml up -d
```

---

## Checklist

### Pre-Deployment
- [ ] Update SECRET_KEY
- [ ] Change default passwords
- [ ] Configure CORS for production domain
- [ ] Set up SSL certificate
- [ ] Configure firewall rules
- [ ] Set up monitoring
- [ ] Configure backups
- [ ] Test in staging environment

### Post-Deployment
- [ ] Verify all services running
- [ ] Test authentication flow
- [ ] Test file upload/download
- [ ] Test WebSocket connection
- [ ] Check logs for errors
- [ ] Verify backups are working
- [ ] Set up alerting
- [ ] Document deployment details

---

For questions or issues, refer to:
- [README.md](README.md) - General documentation
- [DOCKER.md](DOCKER.md) - Docker specifics
- [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md) - Complete feature list
