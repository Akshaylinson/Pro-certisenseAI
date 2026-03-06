#!/bin/bash

echo "🚀 Starting Backend Container..."

# Create data directory
mkdir -p data

# Build backend image
docker build -t certisense-backend ./backend

# Run backend container
docker run -d \
  --name certisense-backend \
  -p 8000:8000 \
  -v $(pwd)/data:/app/data \
  -e DATABASE_URL=sqlite:///data/certisense.db \
  certisense-backend

echo "✅ Backend running at http://localhost:8000"