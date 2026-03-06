@echo off
echo 🚀 Starting CertiSense AI v3.0 with Docker...

REM Create data directory
if not exist "data" mkdir data

REM Build and start containers
docker-compose up --build

echo ✅ CertiSense AI is running!
echo Frontend: http://localhost:5173
echo Backend API: http://localhost:8000
pause