#!/bin/bash

echo "🚀 Starting CertiSense AI v3.0 with Docker..."

# Create data directory
mkdir -p data

# Build and start containers
docker-compose up --build

echo "✅ CertiSense AI is running!"
echo "Frontend: http://localhost:5173"
echo "Backend API: http://localhost:8000"