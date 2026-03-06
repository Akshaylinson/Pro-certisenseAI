#!/bin/bash

echo "🚀 Starting Frontend Container..."

# Build frontend image
docker build -t certisense-frontend ./frontend/web

# Run frontend container
docker run -d \
  --name certisense-frontend \
  -p 5173:5173 \
  -e VITE_API_URL=http://localhost:8000 \
  certisense-frontend

echo "✅ Frontend running at http://localhost:5173"