# 🐳 CertiSense AI v3.0 - Docker Setup

## Container Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Frontend      │    │    Backend      │    │   Database      │
│   (React)       │    │   (FastAPI)     │    │   (SQLite)      │
│   Port: 5173    │◄──►│   Port: 8000    │◄──►│   Volume: data  │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## Quick Start

### Prerequisites
- Docker
- Docker Compose

### 1. Start All Services
```bash
# Linux/Mac
./start-docker.sh

# Windows
start-docker.bat

# Or manually
docker-compose up --build
```

### 2. Access Application
- **Frontend**: http://localhost:5173
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs

### 3. Default Credentials
- **Admin**: username: `admin`, password: `admin123`

## Container Details

### Frontend Container
- **Base**: Node.js 18 Alpine
- **Port**: 5173
- **Environment**: Development mode with hot reload

### Backend Container
- **Base**: Python 3.9 Slim
- **Port**: 8000
- **Database**: SQLite with persistent volume
- **Features**: Auto-reload enabled

### Database Container
- **Type**: SQLite file-based database
- **Storage**: Persistent volume at `./data/certisense.db`
- **Backup**: Database file is accessible on host

## Development

### View Logs
```bash
docker-compose logs -f [service_name]
```

### Rebuild Containers
```bash
docker-compose up --build --force-recreate
```

### Stop Services
```bash
docker-compose down
```

### Database Access
The SQLite database file is located at `./data/certisense.db` and can be accessed directly.

## Production Deployment

For production, update:
1. Change default admin credentials
2. Use environment variables for secrets
3. Configure proper SSL/TLS
4. Set up database backups
5. Use production-ready web server