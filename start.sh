#!/bin/bash

# CSV Browser - Interactive Docker Management Script

# Colors for better UX
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
MAGENTA='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color
BOLD='\033[1m'

# Function to print colored output
print_header() {
    echo -e "${CYAN}${BOLD}"
    echo "=========================================="
    echo "   $1"
    echo "=========================================="
    echo -e "${NC}"
}

print_success() {
    echo -e "${GREEN}✓ $1${NC}"
}

print_error() {
    echo -e "${RED}✗ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠ $1${NC}"
}

print_info() {
    echo -e "${BLUE}ℹ $1${NC}"
}

# Check if Docker is installed
check_docker() {
    if ! command -v docker &> /dev/null; then
        print_error "Docker is not installed"
        echo "Please install Docker from https://docker.com"
        echo "Or install Colima: brew install colima"
        exit 1
    fi

    if ! command -v docker-compose &> /dev/null; then
        print_error "Docker Compose is not installed"
        echo "Please install Docker Compose"
        exit 1
    fi

    # Check if Docker daemon is actually running
    if ! docker ps &>/dev/null; then
        print_error "Docker daemon is not running"
        echo ""

        # Check if using Colima
        if command -v colima &> /dev/null; then
            print_info "Detected Colima installation"
            read -p "Would you like to start Colima? (yes/no): " start_colima

            if [ "$start_colima" == "yes" ]; then
                print_info "Starting Colima..."
                colima start

                # Verify it started
                if docker ps &>/dev/null; then
                    print_success "Colima started successfully!"
                else
                    print_error "Failed to start Colima"
                    exit 1
                fi
            else
                echo "Please start Docker/Colima manually:"
                echo "  colima start"
                echo "Or if using Docker Desktop, start it from Applications"
                exit 1
            fi
        else
            echo "Please start Docker Desktop or run: colima start"
            exit 1
        fi
    fi

    print_success "Docker is installed"
    print_success "Docker Compose is installed"
    print_success "Docker daemon is running"
}

# Check if required ports are available
check_ports() {
    local ports_in_use=()
    local pids_to_kill=()

    # Check each required port
    if lsof -i :3000 &>/dev/null; then
        ports_in_use+=("3000 (Frontend)")
        pids_to_kill+=($(lsof -t -i :3000))
    fi

    if lsof -i :5432 &>/dev/null; then
        ports_in_use+=("5432 (PostgreSQL)")
        pids_to_kill+=($(lsof -t -i :5432))
    fi

    if lsof -i :6379 &>/dev/null; then
        ports_in_use+=("6379 (Redis)")
        pids_to_kill+=($(lsof -t -i :6379))
    fi

    if lsof -i :8000 &>/dev/null; then
        ports_in_use+=("8000 (Backend)")
        pids_to_kill+=($(lsof -t -i :8000))
    fi

    if [ ${#ports_in_use[@]} -gt 0 ]; then
        echo ""
        print_warning "The following ports are already in use:"
        for port in "${ports_in_use[@]}"; do
            echo "  • Port $port"
        done
        echo ""
        read -p "Would you like to free these ports? (yes/no): " free_ports

        if [ "$free_ports" == "yes" ]; then
            # Get unique PIDs
            unique_pids=($(echo "${pids_to_kill[@]}" | tr ' ' '\n' | sort -u))

            print_info "Freeing ports..."
            for pid in "${unique_pids[@]}"; do
                kill "$pid" 2>/dev/null
            done
            sleep 2
            print_success "Ports freed successfully!"
            echo ""
        else
            print_error "Cannot start with ports in use. Exiting."
            return 1
        fi
    fi
    return 0
}

# Start development environment
start_dev() {
    check_ports || return
    print_header "Starting Development Environment"
    print_info "Starting with hot-reload enabled..."
    echo ""
    docker-compose -f docker-compose.dev.yml up --build
}

# Start production environment
start_prod() {
    check_ports || return
    print_header "Starting Production Environment"
    print_info "Starting in detached mode..."
    echo ""
    docker-compose -f docker-compose.prod.yml up --build -d
    echo ""
    print_success "Services started successfully!"
    echo ""
    print_info "Access Points:"
    echo "  • Application: ${CYAN}http://localhost${NC}"
    echo "  • API Docs: ${CYAN}http://localhost:8000/docs${NC}"
    echo ""
    print_info "Default Credentials:"
    echo "  • Username: ${BOLD}admin${NC}"
    echo "  • Password: ${BOLD}admin123${NC}"
    echo ""
    print_warning "Remember to change the admin password!"
}

# Stop all containers
stop_containers() {
    print_header "Stopping All Containers"
    echo ""
    docker-compose -f docker-compose.dev.yml down 2>/dev/null
    docker-compose -f docker-compose.prod.yml down 2>/dev/null
    echo ""
    print_success "All containers stopped"
}

# Rebuild containers
rebuild_containers() {
    print_header "Rebuilding Containers"
    echo ""
    echo "Select environment to rebuild:"
    echo "  1) Development"
    echo "  2) Production"
    echo "  3) Both"
    echo ""
    read -p "Enter choice [1-3]: " rebuild_choice
    echo ""

    case $rebuild_choice in
        1)
            print_info "Rebuilding development containers..."
            docker-compose -f docker-compose.dev.yml build --no-cache
            print_success "Development containers rebuilt!"
            ;;
        2)
            print_info "Rebuilding production containers..."
            docker-compose -f docker-compose.prod.yml build --no-cache
            print_success "Production containers rebuilt!"
            ;;
        3)
            print_info "Rebuilding all containers..."
            docker-compose -f docker-compose.dev.yml build --no-cache
            docker-compose -f docker-compose.prod.yml build --no-cache
            print_success "All containers rebuilt!"
            ;;
        *)
            print_error "Invalid choice"
            ;;
    esac
}

# View logs
view_logs() {
    print_header "View Container Logs"
    echo ""
    echo "Select logs to view:"
    echo "  1) All services"
    echo "  2) Backend only"
    echo "  3) Frontend only"
    echo "  4) PostgreSQL only"
    echo "  5) Redis only"
    echo ""
    read -p "Enter choice [1-5]: " log_choice
    echo ""

    case $log_choice in
        1)
            print_info "Showing all logs (Ctrl+C to exit)..."
            echo ""
            docker-compose -f docker-compose.dev.yml logs -f
            ;;
        2)
            print_info "Showing backend logs (Ctrl+C to exit)..."
            echo ""
            docker-compose -f docker-compose.dev.yml logs -f backend
            ;;
        3)
            print_info "Showing frontend logs (Ctrl+C to exit)..."
            echo ""
            docker-compose -f docker-compose.dev.yml logs -f frontend
            ;;
        4)
            print_info "Showing PostgreSQL logs (Ctrl+C to exit)..."
            echo ""
            docker-compose -f docker-compose.dev.yml logs -f postgres
            ;;
        5)
            print_info "Showing Redis logs (Ctrl+C to exit)..."
            echo ""
            docker-compose -f docker-compose.dev.yml logs -f redis
            ;;
        *)
            print_error "Invalid choice"
            ;;
    esac
}

# Clean everything
clean_all() {
    print_header "Clean All Data"
    echo ""
    print_warning "This will remove all containers, volumes, and uploaded files!"
    read -p "Are you sure? (yes/no): " confirm
    echo ""

    if [ "$confirm" == "yes" ]; then
        print_info "Stopping containers..."
        docker-compose -f docker-compose.dev.yml down -v 2>/dev/null
        docker-compose -f docker-compose.prod.yml down -v 2>/dev/null

        print_info "Removing uploaded files..."
        rm -rf backend/uploads/*
        touch backend/uploads/.gitkeep

        print_success "All data cleaned!"
        print_info "You can now start fresh with option 1 or 2"
    else
        print_info "Clean cancelled"
    fi
}

# Show container status
show_status() {
    print_header "Container Status"
    echo ""

    # Check if any containers are running
    if [ -z "$(docker ps -q -f name=csv_browser)" ]; then
        print_warning "No CSV Browser containers are running"
    else
        print_info "Running containers:"
        echo ""
        docker ps -f name=csv_browser --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"
    fi

    echo ""
    print_info "Docker resource usage:"
    echo ""
    docker stats --no-stream -f name=csv_browser 2>/dev/null || print_warning "No containers running"
}

# Access database shell
db_shell() {
    print_header "PostgreSQL Shell"
    echo ""

    if [ -z "$(docker ps -q -f name=csv_browser_postgres)" ]; then
        print_error "PostgreSQL container is not running"
        print_info "Start the application first (option 1 or 2)"
        return
    fi

    print_info "Connecting to PostgreSQL..."
    print_info "Useful commands:"
    echo "  \\dt          - List tables"
    echo "  \\d users     - Describe users table"
    echo "  SELECT * FROM users;  - View all users"
    echo "  \\q           - Quit"
    echo ""
    docker exec -it csv_browser_postgres psql -U postgres -d csv_browser
}

# Access Redis shell
redis_shell() {
    print_header "Redis CLI"
    echo ""

    if [ -z "$(docker ps -q -f name=csv_browser_redis)" ]; then
        print_error "Redis container is not running"
        print_info "Start the application first (option 1 or 2)"
        return
    fi

    print_info "Connecting to Redis..."
    print_info "Useful commands:"
    echo "  KEYS *       - List all keys"
    echo "  GET key      - Get value"
    echo "  FLUSHALL     - Clear all data"
    echo "  exit         - Quit"
    echo ""
    docker exec -it csv_browser_redis redis-cli
}

# Restart containers
restart_containers() {
    print_header "Restart Containers"
    echo ""
    echo "Select environment to restart:"
    echo "  1) Development"
    echo "  2) Production"
    echo ""
    read -p "Enter choice [1-2]: " restart_choice
    echo ""

    case $restart_choice in
        1)
            print_info "Restarting development containers..."
            docker-compose -f docker-compose.dev.yml restart
            print_success "Development containers restarted!"
            ;;
        2)
            print_info "Restarting production containers..."
            docker-compose -f docker-compose.prod.yml restart
            print_success "Production containers restarted!"
            ;;
        *)
            print_error "Invalid choice"
            ;;
    esac
}

# Check ports status (standalone)
check_ports_status() {
    print_header "Port Status Check"
    echo ""

    local has_conflicts=0

    echo "Checking required ports..."
    echo ""

    # Check port 3000
    if lsof -i :3000 &>/dev/null; then
        print_error "Port 3000 (Frontend) - IN USE"
        has_conflicts=1
    else
        print_success "Port 3000 (Frontend) - Available"
    fi

    # Check port 5432
    if lsof -i :5432 &>/dev/null; then
        print_error "Port 5432 (PostgreSQL) - IN USE"
        has_conflicts=1
    else
        print_success "Port 5432 (PostgreSQL) - Available"
    fi

    # Check port 6379
    if lsof -i :6379 &>/dev/null; then
        print_error "Port 6379 (Redis) - IN USE"
        has_conflicts=1
    else
        print_success "Port 6379 (Redis) - Available"
    fi

    # Check port 8000
    if lsof -i :8000 &>/dev/null; then
        print_error "Port 8000 (Backend) - IN USE"
        has_conflicts=1
    else
        print_success "Port 8000 (Backend) - Available"
    fi

    echo ""

    if [ $has_conflicts -eq 1 ]; then
        print_warning "Some ports are in use!"
        echo ""
        read -p "Would you like to free all conflicting ports? (yes/no): " free_all

        if [ "$free_all" == "yes" ]; then
            check_ports
        fi
    else
        print_success "All ports are available!"
    fi
}

# Backup data
backup_data() {
    print_header "Backup Data"
    echo ""

    if [ -z "$(docker ps -q -f name=csv_browser_postgres)" ]; then
        print_error "PostgreSQL container is not running"
        print_info "Start the application first (option 1 or 2)"
        return
    fi

    BACKUP_DIR="./backups"
    mkdir -p "$BACKUP_DIR"

    DATE=$(date +%Y%m%d_%H%M%S)

    print_info "Creating backup..."

    # Backup database
    print_info "Backing up database..."
    docker exec csv_browser_postgres pg_dump -U postgres csv_browser > "$BACKUP_DIR/db_$DATE.sql"

    # Backup uploads
    print_info "Backing up uploaded files..."
    tar -czf "$BACKUP_DIR/uploads_$DATE.tar.gz" backend/uploads/ 2>/dev/null

    echo ""
    print_success "Backup created successfully!"
    print_info "Files saved to: ${CYAN}$BACKUP_DIR${NC}"
    echo "  • Database: db_$DATE.sql"
    echo "  • Uploads: uploads_$DATE.tar.gz"
}

# View documentation
view_docs() {
    print_header "Documentation"
    echo ""
    echo "Available documentation files:"
    echo ""
    echo "  ${BOLD}1)${NC} README.md          - Main documentation"
    echo "  ${BOLD}2)${NC} QUICKSTART.md      - Quick start guide"
    echo "  ${BOLD}3)${NC} DOCKER.md          - Docker details"
    echo "  ${BOLD}4)${NC} DEPLOYMENT.md      - Deployment guide"
    echo "  ${BOLD}5)${NC} PROJECT_SUMMARY.md - Complete overview"
    echo ""
    read -p "Enter choice to view (or press Enter to skip): " doc_choice

    case $doc_choice in
        1) less README.md ;;
        2) less QUICKSTART.md ;;
        3) less DOCKER.md ;;
        4) less DEPLOYMENT.md ;;
        5) less PROJECT_SUMMARY.md ;;
        *) return ;;
    esac
}

# Main menu
show_menu() {
    clear
    print_header "CSV Browser - Docker Manager"

    echo "🚀 START SERVICES"
    echo "  1) Start Development (hot-reload)"
    echo "  2) Start Production (optimized)"
    echo ""

    echo "🛑 STOP SERVICES"
    echo "  3) Stop All Containers"
    echo "  4) Restart Containers"
    echo ""

    echo "🔧 BUILD & MAINTENANCE"
    echo "  5) Rebuild Containers"
    echo "  6) Clean All Data (reset)"
    echo ""

    echo "📊 MONITORING"
    echo "  7) View Logs"
    echo "  8) Show Container Status"
    echo "  9) Check Port Availability"
    echo ""

    echo "💾 DATABASE"
    echo " 10) PostgreSQL Shell"
    echo " 11) Redis Shell"
    echo " 12) Backup Data"
    echo ""

    echo "📚 HELP"
    echo " 13) View Documentation"
    echo " 14) Show Quick Help"
    echo ""

    echo " 15) Exit"
    echo ""
    echo "=========================================="
    echo ""
}

# Quick help
show_help() {
    print_header "Quick Help"
    echo ""
    echo -e "${BOLD}Getting Started:${NC}"
    echo "  1. Choose option ${GREEN}1${NC} to start development environment"
    echo "  2. Open http://localhost:3000 in your browser"
    echo "  3. Login with username: ${BOLD}admin${NC}, password: ${BOLD}admin123${NC}"
    echo ""
    echo -e "${BOLD}Common Tasks:${NC}"
    echo "  • Start dev: Option ${GREEN}1${NC}"
    echo "  • View logs: Option ${CYAN}7${NC}"
    echo "  • Stop all: Option ${YELLOW}3${NC}"
    echo "  • Clean reset: Option ${BLUE}6${NC}"
    echo ""
    echo -e "${BOLD}Useful URLs:${NC}"
    echo "  • Frontend: ${CYAN}http://localhost:3000${NC}"
    echo "  • Backend API: ${CYAN}http://localhost:8000${NC}"
    echo "  • API Docs: ${CYAN}http://localhost:8000/docs${NC}"
    echo ""
    read -p "Press Enter to continue..."
}

# Main loop
main() {
    # Check prerequisites
    check_docker
    echo ""
    sleep 1

    while true; do
        show_menu
        read -p "Enter your choice [1-15]: " choice
        echo ""

        case $choice in
            1) start_dev ;;
            2) start_prod ;;
            3) stop_containers ;;
            4) restart_containers ;;
            5) rebuild_containers ;;
            6) clean_all ;;
            7) view_logs ;;
            8) show_status ;;
            9) check_ports_status ;;
            10) db_shell ;;
            11) redis_shell ;;
            12) backup_data ;;
            13) view_docs ;;
            14) show_help ;;
            15)
                print_header "Goodbye!"
                print_success "Thank you for using CSV Browser"
                exit 0
                ;;
            *)
                print_error "Invalid choice. Please try again."
                sleep 2
                ;;
        esac

        echo ""
        read -p "Press Enter to return to menu..."
    done
}

# Run main function
main
