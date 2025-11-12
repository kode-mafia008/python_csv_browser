# Interactive Menu Preview

## What It Looks Like

When you run `./start.sh`, you'll see this beautiful interactive menu:

```
==========================================
   CSV Browser - Docker Manager
==========================================

🚀 Start Services
  1) Start Development (hot-reload)
  2) Start Production (optimized)

🛑 Stop Services
  3) Stop All Containers
  4) Restart Containers

🔧 Build & Maintenance
  5) Rebuild Containers
  6) Clean All Data (reset)

📊 Monitoring
  7) View Logs
  8) Show Container Status

💾 Database
  9) PostgreSQL Shell
  10) Redis Shell
  11) Backup Data

📚 Help
  12) View Documentation
  13) Show Quick Help

14) Exit

==========================================

Enter your choice [1-14]:
```

## Color-Coded Output

The menu uses colors for better UX:

- ✅ **Green** - Success messages
- ❌ **Red** - Error messages
- ⚠️ **Yellow** - Warnings
- ℹ️ **Blue** - Information
- 🔵 **Cyan** - Headers and URLs
- 🟣 **Magenta** - Database operations

## Example Sessions

### Starting Development

```
Enter your choice [1-14]: 1

==========================================
   Starting Development Environment
==========================================

ℹ Starting with hot-reload enabled...

Creating network "csv_browser_network"...
Creating csv_browser_postgres...
Creating csv_browser_redis...
Creating csv_browser_backend...
Creating csv_browser_frontend...

✓ All services started!

Press Enter to return to menu...
```

### Viewing Container Status

```
Enter your choice [1-14]: 8

==========================================
   Container Status
==========================================

ℹ Running containers:

NAMES                     STATUS              PORTS
csv_browser_postgres      Up 2 minutes        0.0.0.0:5432->5432/tcp
csv_browser_redis         Up 2 minutes        0.0.0.0:6379->6379/tcp
csv_browser_backend       Up 2 minutes        0.0.0.0:8000->8000/tcp
csv_browser_frontend      Up 2 minutes        0.0.0.0:3000->3000/tcp

ℹ Docker resource usage:

CONTAINER                 CPU %    MEM USAGE / LIMIT     MEM %
csv_browser_postgres      0.15%    45.2MiB / 7.775GiB    0.57%
csv_browser_redis         0.08%    8.1MiB / 7.775GiB     0.10%
csv_browser_backend       1.24%    125.4MiB / 7.775GiB   1.58%
csv_browser_frontend      0.05%    52.3MiB / 7.775GiB    0.66%

Press Enter to return to menu...
```

### Creating a Backup

```
Enter your choice [1-14]: 11

==========================================
   Backup Data
==========================================

ℹ Creating backup...
ℹ Backing up database...
ℹ Backing up uploaded files...

✓ Backup created successfully!
ℹ Files saved to: ./backups
  • Database: db_20250112_143520.sql
  • Uploads: uploads_20250112_143520.tar.gz

Press Enter to return to menu...
```

### Accessing Database Shell

```
Enter your choice [1-14]: 9

==========================================
   PostgreSQL Shell
==========================================

ℹ Connecting to PostgreSQL...
ℹ Useful commands:
  \dt          - List tables
  \d users     - Describe users table
  SELECT * FROM users;  - View all users
  \q           - Quit

psql (15.5)
Type "help" for help.

csv_browser=# \dt
              List of relations
 Schema |    Name    | Type  |  Owner
--------+------------+-------+----------
 public | csv_files  | table | postgres
 public | users      | table | postgres
(2 rows)

csv_browser=# SELECT username, role FROM users;
 username | role
----------+-------
 admin    | admin
 john     | user
 alice    | user
(3 rows)

csv_browser=# \q

Press Enter to return to menu...
```

### Viewing Logs

```
Enter your choice [1-14]: 7

==========================================
   View Container Logs
==========================================

Select logs to view:
  1) All services
  2) Backend only
  3) Frontend only
  4) PostgreSQL only
  5) Redis only

Enter choice [1-5]: 2

ℹ Showing backend logs (Ctrl+C to exit)...

csv_browser_backend | INFO:     Uvicorn running on http://0.0.0.0:8000
csv_browser_backend | INFO:     Application startup complete.
csv_browser_backend | ✓ Redis connected successfully
csv_browser_backend | INFO:     127.0.0.1:52134 - "GET /api/csv HTTP/1.1" 200 OK
csv_browser_backend | INFO:     127.0.0.1:52135 - "POST /api/auth/login HTTP/1.1" 200 OK
csv_browser_backend | INFO:     WebSocket connection established
^C

Press Enter to return to menu...
```

### Rebuilding Containers

```
Enter your choice [1-14]: 5

==========================================
   Rebuilding Containers
==========================================

Select environment to rebuild:
  1) Development
  2) Production
  3) Both

Enter choice [1-3]: 1

ℹ Rebuilding development containers...
Building postgres...
Building redis...
Building backend...
Step 1/10 : FROM python:3.11-slim
Step 2/10 : WORKDIR /app
...
✓ Development containers rebuilt!

Press Enter to return to menu...
```

### Clean Reset

```
Enter your choice [1-14]: 6

==========================================
   Clean All Data
==========================================

⚠ This will remove all containers, volumes, and uploaded files!
Are you sure? (yes/no): yes

ℹ Stopping containers...
Stopping csv_browser_frontend...done
Stopping csv_browser_backend...done
Stopping csv_browser_redis...done
Stopping csv_browser_postgres...done

Removing containers and volumes...
Removing network csv_browser_network

ℹ Removing uploaded files...

✓ All data cleaned!
ℹ You can now start fresh with option 1 or 2

Press Enter to return to menu...
```

### Quick Help

```
Enter your choice [1-14]: 13

==========================================
   Quick Help
==========================================

Getting Started:
  1. Choose option 1 to start development environment
  2. Open http://localhost:3000 in your browser
  3. Login with username: admin, password: admin123

Common Tasks:
  • Start dev: Option 1
  • View logs: Option 7
  • Stop all: Option 3
  • Clean reset: Option 6

Useful URLs:
  • Frontend: http://localhost:3000
  • Backend API: http://localhost:8000
  • API Docs: http://localhost:8000/docs

Press Enter to continue...
```

## Key Features

### 🎨 Visual Design
- Color-coded messages
- Clear section headers
- Emoji indicators
- Consistent formatting

### 🔄 Interactive Flow
- Always returns to main menu
- Clear prompts
- Confirmation for destructive actions
- Helpful error messages

### 🚀 Convenience
- All operations in one place
- No need to remember commands
- Built-in documentation
- Quick access to databases

### 🛡️ Safety
- Confirmation for destructive operations
- Clear warnings
- Reversible actions when possible
- Error handling

## Comparison

### Before (Multiple Commands)

```bash
# Start development
docker-compose -f docker-compose.dev.yml up --build

# In another terminal, view logs
docker-compose -f docker-compose.dev.yml logs -f backend

# In another terminal, access database
docker exec -it csv_browser_postgres psql -U postgres -d csv_browser

# Stop everything
docker-compose -f docker-compose.dev.yml down

# Rebuild
docker-compose -f docker-compose.dev.yml build --no-cache

# Clean everything
docker-compose -f docker-compose.dev.yml down -v
rm -rf backend/uploads/*
```

### After (Interactive Menu)

```bash
# Run menu
./start.sh

# Then just select numbers:
1 - Start dev
7 - View logs
9 - Database shell
3 - Stop
5 - Rebuild
6 - Clean
```

**Result:** 90% less typing, 100% more clarity!

## Tips for Best Experience

1. **Keep terminal wide** - At least 80 characters for best display
2. **Use full-screen** - Easier to read logs and output
3. **Keep menu open** - Run in dedicated terminal window
4. **Learn the numbers** - After a few uses, you'll memorize common options

## Keyboard Shortcuts

| Key | Action |
|-----|--------|
| `1-14` | Select menu option |
| `Enter` | Return to menu |
| `Ctrl+C` | Exit logs / Cancel operation |
| `Ctrl+D` | Exit database/Redis shell |
| `q` | Quit documentation viewer |

## Why This Is Better

1. **Discoverable** - See all available options
2. **Guided** - Clear instructions for each action
3. **Safe** - Confirmations for dangerous operations
4. **Educational** - Helpful commands shown for database shells
5. **Efficient** - No need to remember or look up commands
6. **Professional** - Clean, polished interface
7. **Comprehensive** - Everything you need in one place

## Perfect For

- 🎓 **Beginners** - No Docker knowledge required
- 👨‍💻 **Developers** - Quick access to common operations
- 🎯 **Testing** - Easy to start/stop/rebuild
- 🐛 **Debugging** - Fast access to logs and shells
- 📚 **Learning** - See what commands are available

---

**Try it now!**

```bash
./start.sh
```

**See the magic happen! ✨**
