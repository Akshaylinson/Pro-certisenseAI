#!/bin/bash

echo "🚀 Starting CertiSense AI - Enhanced Blockchain Certificate Verification System"
echo "=================================================================="

# Backend setup
echo "📦 Setting up backend..."
cd backend
python -m uvicorn certisense_main:app --reload --port 8000 &
BACKEND_PID=$!

# Wait for backend to start
sleep 3

# Frontend setup
echo "🌐 Setting up frontend..."
cd ../frontend/web
npm run dev &
FRONTEND_PID=$!

echo ""
echo "✅ CertiSense AI is running!"
echo "📊 Admin Dashboard: http://localhost:5173 (Login: admin/admin123)"
echo "🔍 Verifier Portal: http://localhost:5173 (Register new account)"
echo "🔧 Backend API: http://localhost:8000"
echo ""
echo "🛑 Press Ctrl+C to stop all services"

# Wait for user interrupt
trap "echo '🛑 Stopping services...'; kill $BACKEND_PID $FRONTEND_PID; exit" INT
wait