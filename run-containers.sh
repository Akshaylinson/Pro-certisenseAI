#!/bin/bash

echo "🚀 Starting CertiSense AI v3.0 - Individual Containers..."

# Stop existing containers
docker stop certisense-backend certisense-frontend 2>/dev/null
docker rm certisense-backend certisense-frontend 2>/dev/null

# Create data directory
mkdir -p data

echo "📦 Building Backend Container..."
docker build -t certisense-backend ./backend

echo "📦 Building Frontend Container..."
docker build -t certisense-frontend ./frontend/web

echo "🚀 Starting Backend Container..."
docker run -d \
  --name certisense-backend \
  -p 8000:8000 \
  -v $(pwd)/data:/app/data \
  -e DATABASE_URL=sqlite:///data/certisense.db \
  certisense-backend

echo "🚀 Starting Frontend Container..."
docker run -d \
  --name certisense-frontend \
  -p 5173:5173 \
  -e VITE_API_URL=http://localhost:8000 \
  certisense-frontend

echo "✅ CertiSense AI is running!"
echo "Frontend: http://localhost:5173"
echo "Backend API: http://localhost:8000"
echo ""
echo "To view logs:"
echo "  Backend: docker logs -f certisense-backend"
echo "  Frontend: docker logs -f certisense-frontend"
echo ""
echo "To stop containers:"
echo "  docker stop certisense-backend certisense-frontend"