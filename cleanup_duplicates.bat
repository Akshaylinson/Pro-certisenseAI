@echo off
REM CertiSense AI v3.0 - Duplicate File Cleanup Script (Windows)
REM Phase 5 - System Cleanup

echo ==========================================
echo CertiSense AI v3.0 - Duplicate File Cleanup
echo ==========================================
echo.

REM Create backup
set BACKUP_DIR=..\backup_%date:~-4,4%%date:~-10,2%%date:~-7,2%_%time:~0,2%%time:~3,2%%time:~6,2%
set BACKUP_DIR=%BACKUP_DIR: =0%
echo Creating backup at: %BACKUP_DIR%
mkdir "%BACKUP_DIR%" 2>nul
xcopy /E /I /Q backend "%BACKUP_DIR%\backend\" >nul
echo [OK] Backup created
echo.

REM Remove duplicate main files
echo Removing duplicate main files...
del /F /Q backend\main.py 2>nul && echo   [OK] Removed main.py
del /F /Q backend\server.py 2>nul && echo   [OK] Removed server.py
del /F /Q backend\admin_main.py 2>nul && echo   [OK] Removed admin_main.py
del /F /Q backend\verifier_main.py 2>nul && echo   [OK] Removed verifier_main.py
del /F /Q backend\working_main.py 2>nul && echo   [OK] Removed working_main.py
del /F /Q backend\certisense_minimal.py 2>nul && echo   [OK] Removed certisense_minimal.py
del /F /Q backend\app\main.py 2>nul && echo   [OK] Removed app\main.py
echo.

REM Remove duplicate auth files
echo Removing duplicate auth files...
del /F /Q backend\auth.py 2>nul && echo   [OK] Removed auth.py
del /F /Q backend\verifier_auth.py 2>nul && echo   [OK] Removed verifier_auth.py
echo.

REM Remove duplicate model files
echo Removing duplicate model files...
del /F /Q backend\verifier_models.py 2>nul && echo   [OK] Removed verifier_models.py
del /F /Q backend\app\models\schemas.py 2>nul && echo   [OK] Removed app\models\schemas.py
echo.

REM Remove duplicate API files
echo Removing duplicate API files...
del /F /Q backend\verifier_api.py 2>nul && echo   [OK] Removed verifier_api.py
echo.

REM Remove unused utility files
echo Removing unused utility files...
del /F /Q backend\storage.py 2>nul && echo   [OK] Removed storage.py
del /F /Q backend\simple_test.py 2>nul && echo   [OK] Removed simple_test.py
del /F /Q backend\app\contract_client.py 2>nul && echo   [OK] Removed app\contract_client.py
del /F /Q backend\app\hash_util.py 2>nul && echo   [OK] Removed app\hash_util.py
del /F /Q backend\app\verification_utils.py 2>nul && echo   [OK] Removed app\verification_utils.py
echo.

REM Archive migration files
echo Archiving migration files...
set ARCHIVE_DIR=..\archive
mkdir "%ARCHIVE_DIR%" 2>nul
move backend\verifier_migration.py "%ARCHIVE_DIR%\" 2>nul && echo   [OK] Archived verifier_migration.py
echo.

REM Remove duplicate requirements
echo Removing duplicate requirements...
del /F /Q backend\requirements_fixed.txt 2>nul && echo   [OK] Removed requirements_fixed.txt
del /F /Q backend\requirements_minimal.txt 2>nul && echo   [OK] Removed requirements_minimal.txt
del /F /Q backend\requirements_qwen.txt 2>nul && echo   [OK] Removed requirements_qwen.txt
echo.

echo ==========================================
echo Cleanup Summary
echo ==========================================
echo [OK] Duplicate main files removed: 7
echo [OK] Duplicate auth files removed: 2
echo [OK] Duplicate model files removed: 2
echo [OK] Duplicate API files removed: 1
echo [OK] Unused utility files removed: 5
echo [OK] Duplicate requirements removed: 3
echo [OK] Migration files archived: 1
echo.
echo Total files removed: 20+
echo Backup location: %BACKUP_DIR%
echo.
echo ==========================================
echo Next Steps:
echo ==========================================
echo 1. Test application: cd backend ^&^& python certisense_main.py
echo 2. Verify endpoints: curl http://localhost:8000/health
echo 3. Run frontend: cd frontend\web ^&^& npm run dev
echo.
echo If issues occur, restore from: %BACKUP_DIR%
echo ==========================================
pause
