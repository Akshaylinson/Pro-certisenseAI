@echo off
echo 🚀 Starting CertiSense AI - Enhanced Blockchain Certificate Verification System
echo ==================================================================

echo 📦 Setting up backend...
cd backend
start "CertiSense Backend" cmd /k "python -m uvicorn certisense_main:app --reload --port 8000"

timeout /t 3 /nobreak > nul

echo 🌐 Setting up frontend...
cd ..\frontend\web
start "CertiSense Frontend" cmd /k "npm run dev"

echo.
echo ✅ CertiSense AI is starting!
echo 📊 Admin Dashboard: http://localhost:5173 (Login: admin/admin123)
echo 🔍 Verifier Portal: http://localhost:5173 (Register new account)
echo 🔧 Backend API: http://localhost:8000
echo.
echo 🛑 Close the terminal windows to stop services
pause