@echo off
echo ========================================
echo CertiSense AI v3.0 - Verifier Module Setup
echo ========================================
echo.

echo Step 1: Setting up database...
cd backend
python verifier_migration.py
if %errorlevel% neq 0 (
    echo ERROR: Database setup failed!
    pause
    exit /b 1
)
echo.

echo Step 2: Database setup complete!
echo.

echo ========================================
echo Verifier Module Setup Complete!
echo ========================================
echo.
echo Test Verifier Account Created:
echo   Username: testverifier
echo   Password: verifier123
echo   Email: verifier@test.com
echo.
echo Next Steps:
echo   1. Start backend: run-backend.bat
echo   2. Start frontend: run-frontend.bat
echo   3. Login at http://localhost:5173
echo.
echo API Endpoints Available:
echo   - POST /auth/verifier/login
echo   - POST /api/verifier/verify
echo   - GET /api/verifier/dashboard
echo   - GET /api/verifier/history
echo   - POST /api/verifier/feedback
echo   - GET /api/verifier/blockchain/{hash}
echo   - POST /api/verifier/chatbot
echo.
pause
