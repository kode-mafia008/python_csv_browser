# Quick Setup Guide

## One-Time Setup

### 1. Install PostgreSQL
Make sure PostgreSQL is installed and running on your system.

### 2. Create Database
```bash
createdb csv_browser
```

### 3. Backend Setup
```bash
cd backend

# Create virtual environment
python3 -m venv venv

# Activate it
source venv/bin/activate  # On macOS/Linux
# OR
venv\Scripts\activate  # On Windows

# Install dependencies
pip install -r requirements.txt

# Create .env file
cp .env.example .env

# Initialize database (creates tables and admin user)
python init_db.py
```

### 4. Frontend Setup
```bash
cd frontend

# Install dependencies
npm install
```

## Running the Application

You'll need **two terminal windows**:

### Terminal 1 - Backend
```bash
cd backend
source venv/bin/activate  # Activate virtual environment
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Backend runs at: http://localhost:8000
API Docs: http://localhost:8000/docs

### Terminal 2 - Frontend
```bash
cd frontend
npm run dev
```

Frontend runs at: http://localhost:3000

## First Login

**Admin Account** (created by init_db.py):
- Username: `admin`
- Password: `admin123`

**Create Regular User**:
- Go to http://localhost:3000/signup
- Create a new account (will have "user" role)

## Testing Real-Time Features

1. Open two browser windows
2. Login as admin in one window
3. Login as regular user in the other
4. In admin window: upload the `sample_data.csv` file
5. Watch it appear instantly in the user window!

## Quick Database Reset

If you need to start fresh:
```bash
# Drop and recreate database
dropdb csv_browser
createdb csv_browser

# Re-initialize
cd backend
python init_db.py
```

## Tips

- Use Chrome DevTools Network tab to see WebSocket connection
- Check backend terminal for API request logs
- Use Swagger UI at http://localhost:8000/docs to test API directly
- Sample CSV file included: `sample_data.csv`
