@echo off
echo Starting CertiSense on LOCALHOST...
copy /Y .env.localhost .env
docker-compose down
docker-compose up --build -d
echo.
echo App running at http://localhost:5173
echo API running at http://localhost:8000
