#!/bin/bash
# Run this on your server after filling in .env.server with your IP

echo "Starting CertiSense on SERVER..."
cp .env.server .env
docker compose down
docker compose up --build -d
echo ""
echo "App running at http://$(grep VITE_API_URL .env | cut -d'/' -f3 | cut -d':' -f1):5173"
echo "API running at $(grep VITE_API_URL .env | cut -d'=' -f2)"
