@echo off
echo 🚀 Starting Backend Container...

REM Create data directory
if not exist "data" mkdir data

REM Build backend image
docker build -t certisense-backend ./backend

REM Run backend container
docker run -d --name certisense-backend -p 8000:8000 -v %cd%/data:/app/data -e DATABASE_URL=sqlite:///data/certisense.db certisense-backend

echo ✅ Backend running at http://localhost:8000
pause