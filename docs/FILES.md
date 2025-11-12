# Project Files Overview

Complete list of all files in the CSV Browser project.

## Root Directory

```
.
├── .env.docker              # Docker environment variables
├── .gitignore              # Git ignore rules
├── docker-compose.yml      # Main Docker Compose file
├── docker-compose.dev.yml  # Development Docker Compose
├── docker-compose.prod.yml # Production Docker Compose
├── Makefile                # Helper commands
├── start.sh                # Quick start script (executable)
├── stop.sh                 # Quick stop script (executable)
├── sample_data.csv         # Sample CSV for testing
│
├── DOCKER.md               # Docker setup guide
├── PROJECT_SUMMARY.md      # Project overview
├── QUICKSTART.md           # Quick start guide
├── README.md               # Main documentation
├── SETUP.md                # Manual setup guide
├── TODO                    # Original requirements
└── FILES.md                # This file
```

## Backend (`/backend`)

### Core Application
```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py                      # FastAPI application entry
│   │
│   ├── api/                         # API endpoints
│   │   ├── __init__.py
│   │   ├── auth.py                  # Authentication endpoints
│   │   ├── admin.py                 # Admin-only endpoints
│   │   ├── csv.py                   # CSV file endpoints
│   │   └── websocket.py             # WebSocket endpoint
│   │
│   ├── core/                        # Core functionality
│   │   ├── __init__.py
│   │   ├── config.py                # App configuration
│   │   ├── database.py              # Database connection
│   │   ├── security.py              # JWT & password hashing
│   │   └── deps.py                  # RBAC dependencies
│   │
│   ├── models/                      # SQLAlchemy models
│   │   ├── __init__.py
│   │   ├── user.py                  # User model
│   │   └── csv_file.py              # CSV file model
│   │
│   ├── schemas/                     # Pydantic schemas
│   │   ├── __init__.py
│   │   ├── user.py                  # User schemas
│   │   └── csv_file.py              # CSV file schemas
│   │
│   └── services/                    # Business logic
│       ├── __init__.py
│       ├── user_service.py          # User operations
│       ├── csv_service.py           # CSV operations
│       ├── redis_service.py         # Redis client
│       └── websocket_manager.py     # WebSocket manager
│
├── uploads/                         # CSV file storage
│   └── .gitkeep
│
├── Dockerfile                       # Backend Docker image
├── .dockerignore                    # Docker ignore rules
├── requirements.txt                 # Python dependencies
├── .env.example                     # Environment template
└── init_db.py                       # Database initialization
```

## Frontend (`/frontend`)

### React Application
```
frontend/
├── src/
│   ├── components/                  # React components
│   │   ├── AdminPanel.jsx           # Admin dashboard
│   │   ├── UserPanel.jsx            # User dashboard
│   │   ├── CSVViewer.jsx            # CSV table viewer
│   │   └── ProtectedRoute.jsx       # Route protection
│   │
│   ├── contexts/                    # React contexts
│   │   └── AuthContext.jsx          # Authentication state
│   │
│   ├── hooks/                       # Custom hooks
│   │   └── useWebSocket.js          # WebSocket hook
│   │
│   ├── pages/                       # Page components
│   │   ├── Login.jsx                # Login page
│   │   ├── Signup.jsx               # Signup page
│   │   └── Dashboard.jsx            # Main dashboard
│   │
│   ├── services/                    # API client
│   │   └── api.js                   # Axios API service
│   │
│   ├── App.jsx                      # App component
│   ├── main.jsx                     # React entry point
│   └── index.css                    # Global styles
│
├── public/                          # Static assets
│
├── Dockerfile                       # Production build
├── Dockerfile.dev                   # Development build
├── .dockerignore                    # Docker ignore rules
├── nginx.conf                       # Nginx configuration
├── vite.config.js                   # Vite configuration
├── tailwind.config.js               # Tailwind configuration
├── postcss.config.js                # PostCSS configuration
├── package.json                     # NPM dependencies
├── .env.development                 # Development env vars
└── index.html                       # HTML template
```

## File Count by Type

| Type | Count | Purpose |
|------|-------|---------|
| Python (.py) | 16 | Backend application code |
| JavaScript (.js, .jsx) | 15 | Frontend application code |
| Docker (Dockerfile, .yml) | 6 | Container configuration |
| Documentation (.md) | 6 | Project documentation |
| Configuration | 8 | Build and runtime config |
| Scripts (.sh) | 2 | Helper scripts |
| **Total** | **53+** | **Complete application** |

## Key Files Explained

### Docker & Deployment

**docker-compose.dev.yml**
- Development environment
- Hot-reload enabled
- All ports exposed
- Volume mounts for live coding

**docker-compose.prod.yml**
- Production environment
- Optimized builds
- Nginx serving frontend
- Health checks enabled
- Auto-restart on failure

**.env.docker**
- Environment variables for Docker
- Database connection strings
- Redis URL
- Secret keys

**Makefile**
- Common Docker commands
- Development helpers
- Database access shortcuts

### Backend Core

**app/main.py**
- FastAPI application initialization
- CORS configuration
- Router registration
- Database table creation

**app/core/deps.py**
- `get_current_user()` - JWT validation
- `get_admin_user()` - Admin role check
- `require_role()` - Role-based protection

**app/core/security.py**
- `create_access_token()` - JWT generation
- `verify_password()` - Password verification
- `get_password_hash()` - Password hashing

**app/services/websocket_manager.py**
- WebSocket connection management
- Message broadcasting
- Auto-cleanup of disconnected clients

### Frontend Core

**src/contexts/AuthContext.jsx**
- Global authentication state
- Login/logout functions
- JWT token management
- Role checking

**src/hooks/useWebSocket.js**
- WebSocket connection
- Auto-reconnection
- Message handling
- Connection lifecycle

**src/services/api.js**
- Axios instance
- JWT token injection
- API endpoint definitions
- Error handling

### Configuration Files

**backend/requirements.txt**
- FastAPI and dependencies
- Database drivers (psycopg2, redis)
- Security libraries (jose, passlib)
- Python packages

**frontend/package.json**
- React and dependencies
- Build tools (Vite)
- Styling (Tailwind)
- Development dependencies

**vite.config.js**
- Development server config
- Proxy settings for API
- Build optimization

**nginx.conf**
- Production web server config
- API proxy rules
- WebSocket proxy
- Static file serving
- Gzip compression

## Documentation Files

**README.md**
- Project overview
- Quick start with Docker
- Features list
- Both Docker and manual setup
- API documentation
- Troubleshooting

**DOCKER.md**
- Detailed Docker guide
- Architecture diagram
- Service descriptions
- Commands reference
- Production deployment
- Security considerations

**QUICKSTART.md**
- Minimal getting started guide
- Three different start methods
- Common tasks
- Troubleshooting
- First steps tutorial

**SETUP.md**
- Manual installation guide
- Database setup
- Backend configuration
- Frontend configuration
- Testing real-time features

**PROJECT_SUMMARY.md**
- Complete feature list
- Architecture overview
- Design decisions
- API endpoints
- Compliance checklist
- Future enhancements

## Adding New Files

### New Backend Endpoint
```
1. Create route in backend/app/api/
2. Add service logic in backend/app/services/
3. Update schemas in backend/app/schemas/
4. Register router in backend/app/main.py
```

### New Frontend Page
```
1. Create component in frontend/src/pages/
2. Add route in frontend/src/App.jsx
3. Update navigation in components
4. Add API calls in frontend/src/services/api.js
```

### New Docker Service
```
1. Add service to docker-compose.*.yml
2. Update environment variables
3. Update Makefile if needed
4. Document in DOCKER.md
```

## File Permissions

Executable files:
- `start.sh` - Quick start script
- `stop.sh` - Quick stop script

Set with: `chmod +x start.sh stop.sh`

## Version Control

**.gitignore** excludes:
- Python cache files (`__pycache__`)
- Virtual environments (`venv/`)
- Environment files (`.env`)
- Node modules (`node_modules/`)
- Build outputs (`dist/`, `build/`)
- IDE files (`.vscode/`, `.idea/`)
- Uploaded CSV files (except `.gitkeep`)
- Docker overrides

## File Size Estimates

| Component | Size |
|-----------|------|
| Backend code | ~50 KB |
| Frontend code | ~80 KB |
| Documentation | ~100 KB |
| Docker config | ~10 KB |
| Dependencies (node_modules) | ~200 MB |
| Dependencies (Python venv) | ~100 MB |
| Docker images | ~1-2 GB |
| Database volume | Varies |

## Maintenance

### Regular Updates
- `requirements.txt` - Python packages
- `package.json` - NPM packages
- Docker base images
- Documentation

### Code Quality
- All Python files use type hints
- All components are documented
- Services follow single responsibility
- Proper error handling throughout
