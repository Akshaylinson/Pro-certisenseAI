#!/bin/bash

echo "🔐 CertiSense AI v3.0 - Admin Module Startup"
echo "============================================"

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8+"
    exit 1
fi

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo "❌ Node.js is not installed. Please install Node.js 16+"
    exit 1
fi

echo "✅ Prerequisites check passed"
echo ""

# Backend Setup
echo "📦 Setting up Backend..."
cd backend

if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

source venv/bin/activate
pip install -q fastapi uvicorn sqlalchemy pydantic python-jose[cryptography] python-multipart

echo "✅ Backend dependencies installed"
echo ""

# Start Backend
echo "🚀 Starting Admin Backend Server..."
python admin_main.py &
BACKEND_PID=$!
echo "Backend running on http://localhost:8000 (PID: $BACKEND_PID)"
echo ""

# Frontend Setup
echo "📦 Setting up Frontend..."
cd ../frontend/web

if [ ! -d "node_modules" ]; then
    echo "Installing frontend dependencies..."
    npm install
fi

echo "✅ Frontend dependencies installed"
echo ""

# Start Frontend
echo "🚀 Starting Admin Frontend..."
npm run dev &
FRONTEND_PID=$!
echo "Frontend running on http://localhost:5173 (PID: $FRONTEND_PID)"
echo ""

echo "============================================"
echo "✅ CertiSense AI v3.0 Admin Module is running!"
echo ""
echo "📊 Admin Dashboard: http://localhost:5173"
echo "🔌 Backend API: http://localhost:8000"
echo "📚 API Docs: http://localhost:8000/docs"
echo ""
echo "🔐 Default Admin Credentials:"
echo "   Username: admin"
echo "   Password: admin123"
echo ""
echo "Press Ctrl+C to stop all services"
echo "============================================"

# Wait for user interrupt
trap "kill $BACKEND_PID $FRONTEND_PID; exit" INT
wait
