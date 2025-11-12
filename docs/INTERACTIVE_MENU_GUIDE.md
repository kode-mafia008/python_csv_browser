# Interactive Menu Guide

The CSV Browser includes a powerful interactive menu script (`start.sh`) that provides a user-friendly interface for managing all Docker operations.

## Starting the Menu

```bash
./start.sh
```

## Menu Overview

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
```

## Feature Details

### 🚀 Start Services

#### 1) Start Development
- Starts all services with hot-reload
- Backend: FastAPI with auto-reload on code changes
- Frontend: Vite dev server with HMR (Hot Module Replacement)
- Runs in foreground (see logs in real-time)
- Access at: http://localhost:3000

**When to use:**
- Active development
- Testing new features
- Debugging issues

#### 2) Start Production
- Starts optimized production build
- Nginx serving frontend
- Multiple uvicorn workers
- Runs in background (detached mode)
- Access at: http://localhost

**When to use:**
- Testing production build
- Deployment simulation
- Performance testing

---

### 🛑 Stop Services

#### 3) Stop All Containers
- Stops both dev and prod containers
- Preserves data (volumes remain)
- Can restart later without data loss

**Use case:**
- Temporarily stopping the application
- Switching between dev/prod
- Freeing up system resources

#### 4) Restart Containers
- Choose dev or prod environment
- Quick restart without rebuilding
- Useful after config changes

**Sub-options:**
```
1) Development
2) Production
```

**Use case:**
- Applied .env changes
- Network issues
- Service hang/freeze

---

### 🔧 Build & Maintenance

#### 5) Rebuild Containers
- Rebuild from scratch (no cache)
- Choose which environment to rebuild

**Sub-options:**
```
1) Development
2) Production
3) Both
```

**When to rebuild:**
- Changed Dockerfile
- Updated dependencies (requirements.txt, package.json)
- Corrupted image
- Want clean build

#### 6) Clean All Data
- **DESTRUCTIVE OPERATION**
- Removes all containers and volumes
- Deletes uploaded CSV files
- Requires confirmation

**Confirmation required:** Type `yes`

**Use case:**
- Start completely fresh
- Clear test data
- Reset database
- Troubleshooting persistent issues

---

### 📊 Monitoring

#### 7) View Logs
- Real-time log streaming
- Filter by service

**Sub-options:**
```
1) All services        - Everything
2) Backend only        - FastAPI logs
3) Frontend only       - React/Vite logs
4) PostgreSQL only     - Database logs
5) Redis only          - Cache logs
```

**Exit logs:** Press `Ctrl+C`

**Use case:**
- Debugging errors
- Monitoring activity
- Performance analysis

#### 8) Show Container Status
- List running containers
- Show resource usage (CPU, Memory)
- Port mappings
- Container health

**Output includes:**
```
Container Name    Status         Ports
Resource usage    CPU%    Memory
```

**Use case:**
- Check if containers are running
- Monitor resource consumption
- Verify port mappings

---

### 💾 Database

#### 9) PostgreSQL Shell
- Direct access to database
- Run SQL queries
- Inspect data

**Provided commands:**
```sql
\dt                    -- List all tables
\d users               -- Describe users table
SELECT * FROM users;   -- View all users
\q                     -- Quit
```

**Example session:**
```sql
csv_browser=# SELECT username, role FROM users;
 username | role
----------+-------
 admin    | admin
 john     | user
```

**Use case:**
- View database contents
- Run custom queries
- Debug data issues
- Manual data manipulation

#### 10) Redis Shell
- Direct access to Redis
- Inspect cached data
- Clear cache

**Provided commands:**
```
KEYS *         -- List all keys
GET key        -- Get value for key
SET key value  -- Set a value
FLUSHALL       -- Clear all data
exit           -- Quit
```

**Example session:**
```
127.0.0.1:6379> KEYS *
1) "session:abc123"
2) "cache:csv_list"
```

**Use case:**
- Inspect cached data
- Debug caching issues
- Clear cache manually
- Test Redis features

#### 11) Backup Data
- Automated backup creation
- Backs up PostgreSQL database
- Backs up uploaded CSV files
- Timestamped filenames

**Backup location:** `./backups/`

**Files created:**
- `db_YYYYMMDD_HHMMSS.sql` - Database dump
- `uploads_YYYYMMDD_HHMMSS.tar.gz` - Uploaded files

**Example:**
```
✓ Backup created successfully!
ℹ Files saved to: ./backups
  • Database: db_20250112_143022.sql
  • Uploads: uploads_20250112_143022.tar.gz
```

**Use case:**
- Before major changes
- Regular backups
- Data migration
- Disaster recovery

---

### 📚 Help

#### 12) View Documentation
- Browse documentation files
- Quick reference

**Available docs:**
```
1) README.md          - Main documentation
2) QUICKSTART.md      - Quick start guide
3) DOCKER.md          - Docker details
4) DEPLOYMENT.md      - Deployment guide
5) PROJECT_SUMMARY.md - Complete overview
```

**Navigation:**
- Scroll: Arrow keys or Page Up/Down
- Search: `/` then type search term
- Quit: Press `q`

#### 13) Show Quick Help
- Getting started guide
- Common tasks reference
- Useful URLs
- Keyboard shortcuts

**Displays:**
- How to start
- Default credentials
- Common operations
- Access URLs

---

## Color Coding

The menu uses colors for better readability:

- 🟢 **Green** - Success messages, start operations
- 🟡 **Yellow** - Warnings, stop operations
- 🔵 **Blue** - Info messages, build operations
- 🟣 **Magenta** - Database operations
- 🔴 **Red** - Errors, destructive operations
- ⚪ **Cyan** - Headers, URLs

## Keyboard Shortcuts

- **Enter** - Return to menu
- **Ctrl+C** - Exit logs view or stop operation
- **Ctrl+D** - Exit database/Redis shell
- **q** - Quit documentation viewer

## Common Workflows

### First Time Setup
```
1. Run: ./start.sh
2. Choose: Option 1 (Start Development)
3. Wait for: "✓ Services started"
4. Open: http://localhost:3000
5. Login: admin / admin123
```

### Daily Development
```
1. Start: Option 1
2. Make code changes
3. View logs: Option 7 (if needed)
4. Stop: Ctrl+C (in terminal) or Option 3
```

### Check if Running
```
1. Choose: Option 8 (Show Container Status)
2. View: Running containers and resources
3. Return to menu
```

### Debug Issues
```
1. View logs: Option 7
2. Select service to debug
3. Look for errors
4. If needed: Option 5 (Rebuild) or Option 6 (Clean)
```

### Database Inspection
```
1. Start services: Option 1 or 2
2. Open DB shell: Option 9
3. Run queries
4. Exit: \q
```

### Create Backup
```
1. Ensure running: Option 8
2. Create backup: Option 11
3. Files saved to: ./backups/
```

### Production Testing
```
1. Build prod: Option 5 → 2
2. Start prod: Option 2
3. Test at: http://localhost
4. View logs: Option 7 (if issues)
5. Stop: Option 3
```

### Complete Reset
```
1. Stop all: Option 3
2. Clean data: Option 6 → yes
3. Rebuild: Option 5 → 3
4. Start fresh: Option 1
```

## Tips & Tricks

### Tip 1: Multiple Terminals
Run start.sh in one terminal for the menu, and keep logs open in another:
```bash
# Terminal 1
./start.sh

# Terminal 2
docker-compose -f docker-compose.dev.yml logs -f
```

### Tip 2: Quick Status Check
Before making changes, check container status to ensure everything is running.

### Tip 3: Regular Backups
Create backups before:
- Major code changes
- Database migrations
- Production deployments
- Experimenting with new features

### Tip 4: Log Filtering
Use grep to filter logs:
```bash
docker-compose -f docker-compose.dev.yml logs -f backend | grep ERROR
```

### Tip 5: Resource Monitoring
Keep an eye on resources with Option 8 if experiencing performance issues.

## Troubleshooting

### Menu Won't Start
```bash
# Check if script is executable
ls -la start.sh

# If not, make it executable
chmod +x start.sh

# Run again
./start.sh
```

### Docker Not Found
```
✗ Docker is not installed
```
**Solution:** Install Docker Desktop from https://docker.com

### Port Already in Use
**Error in logs:** "Address already in use"

**Solution:**
1. Stop conflicting service
2. Or change port in docker-compose.yml

### Containers Won't Stop
```bash
# Force stop
docker stop $(docker ps -q -f name=csv_browser)

# Force remove
docker rm -f $(docker ps -aq -f name=csv_browser)
```

### Clean Not Working
```bash
# Manual cleanup
docker-compose -f docker-compose.dev.yml down -v --remove-orphans
docker-compose -f docker-compose.prod.yml down -v --remove-orphans
rm -rf backend/uploads/*
docker system prune -a --volumes
```

## Advanced Usage

### Environment Variables
Set before running menu:
```bash
export POSTGRES_PASSWORD=mysecretpassword
./start.sh
```

### Custom Compose Files
Modify menu to use custom compose file:
Edit start.sh and change compose file references.

### Automated Scripts
Use menu functions in your own scripts:
```bash
# Source the functions
source start.sh

# Call specific function
start_dev
```

## Exit Codes

The script uses standard exit codes:
- `0` - Success
- `1` - Error (Docker not found, invalid choice, etc.)

## Support

If you encounter issues:
1. Check logs: Option 7
2. View status: Option 8
3. Try rebuild: Option 5
4. Last resort: Clean and restart (Option 6)

Still stuck? Check the documentation or create an issue.

---

**Enjoy the interactive experience!** 🎉
