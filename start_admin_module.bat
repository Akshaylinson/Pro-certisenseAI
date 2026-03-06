@echo off
echo ============================================
echo 🔐 CertiSense AI v3.0 - Admin Module Startup
echo ============================================
echo.

REM Check Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is not installed. Please install Python 3.8+
    pause
    exit /b 1
)

REM Check Node.js
node --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Node.js is not installed. Please install Node.js 16+
    pause
    exit /b 1
)

echo ✅ Prerequisites check passed
echo.

REM Backend Setup
echo 📦 Setting up Backend...
cd backend

if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
)

call venv\Scripts\activate.bat
pip install -q fastapi uvicorn sqlalchemy pydantic python-jose[cryptography] python-multipart

echo ✅ Backend dependencies installed
echo.

REM Start Backend
echo 🚀 Starting Admin Backend Server...
start "CertiSense Backend" cmd /k "venv\Scripts\activate.bat && python admin_main.py"
timeout /t 3 >nul
echo Backend running on http://localhost:8000
echo.

REM Frontend Setup
echo 📦 Setting up Frontend...
cd ..\frontend\web

if not exist "node_modules" (
    echo Installing frontend dependencies...
    call npm install
)

echo ✅ Frontend dependencies installed
echo.

REM Start Frontend
echo 🚀 Starting Admin Frontend...
start "CertiSense Frontend" cmd /k "npm run dev"
timeout /t 3 >nul
echo Frontend running on http://localhost:5173
echo.

echo ============================================
echo ✅ CertiSense AI v3.0 Admin Module is running!
echo.
echo 📊 Admin Dashboard: http://localhost:5173
echo 🔌 Backend API: http://localhost:8000
echo 📚 API Docs: http://localhost:8000/docs
echo.
echo 🔐 Default Admin Credentials:
echo    Username: admin
echo    Password: admin123
echo.
echo Close the terminal windows to stop services
echo ============================================
echo.
pause
