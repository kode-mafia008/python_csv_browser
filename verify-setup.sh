#!/bin/bash

# CSV Browser - Setup Verification Script

echo "======================================"
echo "   CSV Browser - Setup Verification"
echo "======================================"
echo ""

errors=0
warnings=0

# Function to check if a file exists
check_file() {
    if [ -f "$1" ]; then
        echo "✓ $1"
    else
        echo "✗ $1 (missing)"
        ((errors++))
    fi
}

# Function to check if a directory exists
check_dir() {
    if [ -d "$1" ]; then
        echo "✓ $1/"
    else
        echo "✗ $1/ (missing)"
        ((errors++))
    fi
}

echo "Checking Docker files..."
check_file "docker-compose.yml"
check_file "docker-compose.dev.yml"
check_file "docker-compose.prod.yml"
check_file ".env.docker"
check_file "Makefile"
echo ""

echo "Checking backend files..."
check_dir "backend"
check_file "backend/Dockerfile"
check_file "backend/requirements.txt"
check_file "backend/init_db.py"
check_file "backend/app/main.py"
check_file "backend/app/core/config.py"
check_file "backend/app/core/database.py"
check_file "backend/app/core/security.py"
check_file "backend/app/core/deps.py"
check_file "backend/app/api/auth.py"
check_file "backend/app/api/admin.py"
check_file "backend/app/api/csv.py"
check_file "backend/app/api/websocket.py"
echo ""

echo "Checking frontend files..."
check_dir "frontend"
check_file "frontend/Dockerfile"
check_file "frontend/Dockerfile.dev"
check_file "frontend/package.json"
check_file "frontend/vite.config.js"
check_file "frontend/nginx.conf"
check_file "frontend/src/main.jsx"
check_file "frontend/src/App.jsx"
check_file "frontend/src/contexts/AuthContext.jsx"
check_file "frontend/src/hooks/useWebSocket.js"
check_file "frontend/src/services/api.js"
echo ""

echo "Checking documentation..."
check_file "README.md"
check_file "DOCKER.md"
check_file "QUICKSTART.md"
check_file "SETUP.md"
check_file "PROJECT_SUMMARY.md"
echo ""

echo "Checking scripts..."
if [ -x "start.sh" ]; then
    echo "✓ start.sh (executable)"
else
    echo "⚠ start.sh (not executable - run: chmod +x start.sh)"
    ((warnings++))
fi

if [ -x "stop.sh" ]; then
    echo "✓ stop.sh (executable)"
else
    echo "⚠ stop.sh (not executable - run: chmod +x stop.sh)"
    ((warnings++))
fi
echo ""

# Check for Docker
echo "Checking system requirements..."
if command -v docker &> /dev/null; then
    echo "✓ Docker is installed ($(docker --version))"
else
    echo "✗ Docker is NOT installed"
    ((errors++))
fi

if command -v docker-compose &> /dev/null; then
    echo "✓ Docker Compose is installed ($(docker-compose --version))"
else
    echo "✗ Docker Compose is NOT installed"
    ((errors++))
fi
echo ""

# Summary
echo "======================================"
echo "Summary:"
echo "  Errors: $errors"
echo "  Warnings: $warnings"
echo "======================================"
echo ""

if [ $errors -eq 0 ] && [ $warnings -eq 0 ]; then
    echo "✓ All checks passed! You're ready to start."
    echo ""
    echo "Next steps:"
    echo "  1. Run: ./start.sh"
    echo "  2. Open: http://localhost:3000"
    echo "  3. Login: admin / admin123"
    exit 0
elif [ $errors -eq 0 ]; then
    echo "⚠ Setup is mostly complete, but there are some warnings."
    echo "The application should still work."
    exit 0
else
    echo "✗ Setup verification failed with $errors error(s)."
    echo "Please check the missing files above."
    exit 1
fi
