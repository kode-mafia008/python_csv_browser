# CSV Browser - Full-Stack Web Application

A real-time CSV browser with role-based access control (RBAC) built with FastAPI and React.

## Quick Start with Docker (Recommended)

### Interactive Menu (Easiest!)

```bash
./start.sh
```

This launches a colorful interactive menu with 14 options:
- 🚀 Start Development/Production
- 🛑 Stop/Restart Containers
- 🔧 Rebuild/Clean
- 📊 View Logs/Status
- 💾 Database/Redis Shell
- 📚 Backup & Documentation

See [INTERACTIVE_MENU_GUIDE.md](INTERACTIVE_MENU_GUIDE.md) for full details.

### Command Line

```bash
# Start development environment
make dev

# Or using docker-compose directly
docker-compose -f docker-compose.dev.yml up --build
```

### Access the Application

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000/docs
- **Default Login**: `admin` / `admin123`

For detailed Docker instructions, see [DOCKER.md](DOCKER.md)

## Features

- **Authentication & Authorization**: JWT-based authentication with role-based access control (Admin/User)
- **Real-Time Updates**: WebSocket integration for instant updates across all connected clients
- **Admin Panel**:
  - Upload and delete CSV files
  - Manage users (view and delete)
  - View all uploaded files with metadata
- **User Panel**:
  - Browse available CSV files
  - View CSV contents in a table format
  - Download CSV files
- **Real-Time Sync**: All clients receive instant updates when files are uploaded or deleted

## Tech Stack

### Backend
- **FastAPI** - Modern Python web framework
- **PostgreSQL** - Relational database
- **Redis** - Caching and session management
- **SQLAlchemy** - ORM for database operations
- **JWT** - Token-based authentication
- **WebSockets** - Real-time communication

### Frontend
- **React** - UI library
- **Vite** - Build tool
- **Tailwind CSS** - Styling
- **Axios** - HTTP client
- **React Router** - Navigation

### Infrastructure
- **Docker** - Containerization
- **Docker Compose** - Multi-container orchestration
- **Nginx** - Production web server

## Project Structure

```
csv-browser/
├── backend/
│   ├── app/
│   │   ├── api/           # API route handlers
│   │   │   ├── auth.py    # Authentication endpoints
│   │   │   ├── admin.py   # Admin-only endpoints
│   │   │   ├── csv.py     # CSV file endpoints
│   │   │   └── websocket.py
│   │   ├── core/          # Core functionality
│   │   │   ├── config.py  # Configuration
│   │   │   ├── database.py
│   │   │   ├── security.py # JWT & password hashing
│   │   │   └── deps.py    # RBAC dependencies
│   │   ├── models/        # Database models
│   │   │   ├── user.py
│   │   │   └── csv_file.py
│   │   ├── schemas/       # Pydantic schemas
│   │   ├── services/      # Business logic
│   │   └── main.py        # FastAPI application
│   ├── uploads/           # CSV file storage
│   ├── requirements.txt
│   └── init_db.py         # Database initialization
├── frontend/
│   ├── src/
│   │   ├── components/    # React components
│   │   ├── contexts/      # React contexts (Auth)
│   │   ├── hooks/         # Custom hooks (WebSocket)
│   │   ├── pages/         # Page components
│   │   ├── services/      # API services
│   │   └── main.jsx
│   └── package.json
└── README.md
```

## Setup Instructions

### Option 1: Docker Setup (Recommended)

**Prerequisites:**
- Docker Engine 20.10+
- Docker Compose 2.0+

**Quick Start:**
```bash
# Development mode with hot-reload
make dev

# Production mode
make prod

# View logs
make logs

# Stop containers
make down
```

See [DOCKER.md](DOCKER.md) for detailed Docker instructions.

---

### Option 2: Manual Setup

**Prerequisites:**
- Python 3.9+
- Node.js 18+
- PostgreSQL 12+
- Redis 6+ (optional)

### 1. Database Setup

Create a PostgreSQL database:

```bash
# Using psql
createdb csv_browser

# Or using PostgreSQL command line
psql -U postgres
CREATE DATABASE csv_browser;
```

### 2. Backend Setup

```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
cp .env.example .env

# Edit .env file with your database credentials
# DATABASE_URL=postgresql://username:password@localhost:5432/csv_browser

# Initialize database and create admin user
python init_db.py

# Run the backend server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

The backend will be running at `http://localhost:8000`

### 3. Frontend Setup

```bash
# Open a new terminal
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Run the development server
npm run dev
```

The frontend will be running at `http://localhost:3000`

## Default Credentials

After running `init_db.py`, an admin account is created:

- **Username**: `admin`
- **Password**: `admin123`

**Important**: Change the admin password in production!

## API Endpoints

### Authentication
- `POST /api/auth/signup` - Create new user account
- `POST /api/auth/login` - Login and get JWT token

### CSV Files (Authenticated Users)
- `GET /api/csv` - Get all CSV files
- `GET /api/csv/{file_id}` - Get CSV file content as JSON
- `GET /api/csv/{file_id}/download` - Download CSV file

### Admin Only
- `POST /api/admin/csv/upload` - Upload new CSV file
- `DELETE /api/admin/csv/{file_id}` - Delete CSV file
- `GET /api/admin/users` - Get all users
- `DELETE /api/admin/users/{user_id}` - Delete user

### WebSocket
- `WS /ws` - WebSocket endpoint for real-time updates

## Usage

### For Regular Users

1. **Sign Up**: Create a new account at `/signup`
2. **Login**: Sign in with your credentials
3. **Browse Files**: View all available CSV files
4. **View Content**: Click "View" to see the CSV data in a table
5. **Download**: Download any CSV file for offline use

### For Admins

1. **Login**: Use admin credentials
2. **Upload Files**: Upload CSV files via the admin panel
3. **Manage Files**: View and delete CSV files
4. **Manage Users**: View and delete user accounts
5. **Real-Time Updates**: All changes are broadcast to connected clients instantly

## Real-Time Features

The application uses WebSockets to provide real-time updates:

- When an admin uploads a CSV file, all connected users see it immediately
- When an admin deletes a CSV file, it's removed from all users' views instantly
- No manual refresh required

## Security Features

1. **JWT Authentication**: Secure token-based authentication
2. **Role-Based Access Control**: Admin and User roles with different permissions
3. **Password Hashing**: Passwords are hashed using bcrypt
4. **Protected Routes**: Backend endpoints protected by FastAPI dependencies
5. **CORS Configuration**: Configured for secure cross-origin requests

## Development

### Backend

```bash
# Run with auto-reload
uvicorn app.main:app --reload

# Access API documentation
# Swagger UI: http://localhost:8000/docs
# ReDoc: http://localhost:8000/redoc
```

### Frontend

```bash
# Run development server
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview
```

## Testing

### Manual Testing

1. **Test Authentication**:
   - Sign up with a new user
   - Login with admin credentials
   - Verify JWT token is stored

2. **Test CSV Upload** (Admin):
   - Upload a CSV file
   - Verify it appears in the list
   - Check real-time update in another browser tab

3. **Test CSV Viewing** (User):
   - Login as regular user
   - View CSV files
   - Download a file

4. **Test User Management** (Admin):
   - View all users
   - Delete a user (except admin)

## Troubleshooting

### Backend Issues

**Database Connection Error**:
- Verify PostgreSQL is running
- Check DATABASE_URL in .env file
- Ensure database exists

**Import Errors**:
- Activate virtual environment
- Reinstall dependencies: `pip install -r requirements.txt`

**WebSocket Connection Failed**:
- Check if backend is running
- Verify CORS settings in main.py

### Frontend Issues

**API Connection Error**:
- Verify backend is running on port 8000
- Check proxy configuration in vite.config.js

**WebSocket Not Connecting**:
- Check WebSocket URL in useWebSocket.js
- Verify backend WebSocket endpoint is accessible

## Production Deployment

### Backend

1. Set strong SECRET_KEY in environment variables
2. Use production database credentials
3. Enable HTTPS
4. Configure proper CORS origins
5. Use production ASGI server (uvicorn with workers)

### Frontend

1. Build production bundle: `npm run build`
2. Serve static files with nginx/Apache
3. Configure environment variables
4. Enable HTTPS

## License

MIT License

## Author

Built as part of a full-stack development assignment.
