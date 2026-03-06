@echo off
REM CertiSense AI v3.0 - Cleanup Verification Script
REM Verifies that duplicate files were successfully removed

echo ==========================================
echo CertiSense AI v3.0 - Cleanup Verification
echo ==========================================
echo.

set PASS=0
set FAIL=0
set TOTAL=0

REM Check that duplicate files are removed
echo Checking duplicate files were removed...
echo.

REM Duplicate main files
set /a TOTAL+=7
if exist backend\main.py (echo [FAIL] main.py still exists & set /a FAIL+=1) else (echo [PASS] main.py removed & set /a PASS+=1)
if exist backend\server.py (echo [FAIL] server.py still exists & set /a FAIL+=1) else (echo [PASS] server.py removed & set /a PASS+=1)
if exist backend\admin_main.py (echo [FAIL] admin_main.py still exists & set /a FAIL+=1) else (echo [PASS] admin_main.py removed & set /a PASS+=1)
if exist backend\verifier_main.py (echo [FAIL] verifier_main.py still exists & set /a FAIL+=1) else (echo [PASS] verifier_main.py removed & set /a PASS+=1)
if exist backend\working_main.py (echo [FAIL] working_main.py still exists & set /a FAIL+=1) else (echo [PASS] working_main.py removed & set /a PASS+=1)
if exist backend\certisense_minimal.py (echo [FAIL] certisense_minimal.py still exists & set /a FAIL+=1) else (echo [PASS] certisense_minimal.py removed & set /a PASS+=1)
if exist backend\app\main.py (echo [FAIL] app\main.py still exists & set /a FAIL+=1) else (echo [PASS] app\main.py removed & set /a PASS+=1)

echo.
REM Duplicate auth files
set /a TOTAL+=2
if exist backend\auth.py (echo [FAIL] auth.py still exists & set /a FAIL+=1) else (echo [PASS] auth.py removed & set /a PASS+=1)
if exist backend\verifier_auth.py (echo [FAIL] verifier_auth.py still exists & set /a FAIL+=1) else (echo [PASS] verifier_auth.py removed & set /a PASS+=1)

echo.
REM Duplicate model files
set /a TOTAL+=2
if exist backend\verifier_models.py (echo [FAIL] verifier_models.py still exists & set /a FAIL+=1) else (echo [PASS] verifier_models.py removed & set /a PASS+=1)
if exist backend\app\models\schemas.py (echo [FAIL] app\models\schemas.py still exists & set /a FAIL+=1) else (echo [PASS] app\models\schemas.py removed & set /a PASS+=1)

echo.
REM Duplicate API files
set /a TOTAL+=1
if exist backend\verifier_api.py (echo [FAIL] verifier_api.py still exists & set /a FAIL+=1) else (echo [PASS] verifier_api.py removed & set /a PASS+=1)

echo.
REM Unused utility files
set /a TOTAL+=5
if exist backend\storage.py (echo [FAIL] storage.py still exists & set /a FAIL+=1) else (echo [PASS] storage.py removed & set /a PASS+=1)
if exist backend\simple_test.py (echo [FAIL] simple_test.py still exists & set /a FAIL+=1) else (echo [PASS] simple_test.py removed & set /a PASS+=1)
if exist backend\app\contract_client.py (echo [FAIL] app\contract_client.py still exists & set /a FAIL+=1) else (echo [PASS] app\contract_client.py removed & set /a PASS+=1)
if exist backend\app\hash_util.py (echo [FAIL] app\hash_util.py still exists & set /a FAIL+=1) else (echo [PASS] app\hash_util.py removed & set /a PASS+=1)
if exist backend\app\verification_utils.py (echo [FAIL] app\verification_utils.py still exists & set /a FAIL+=1) else (echo [PASS] app\verification_utils.py removed & set /a PASS+=1)

echo.
REM Duplicate requirements
set /a TOTAL+=3
if exist backend\requirements_fixed.txt (echo [FAIL] requirements_fixed.txt still exists & set /a FAIL+=1) else (echo [PASS] requirements_fixed.txt removed & set /a PASS+=1)
if exist backend\requirements_minimal.txt (echo [FAIL] requirements_minimal.txt still exists & set /a FAIL+=1) else (echo [PASS] requirements_minimal.txt removed & set /a PASS+=1)
if exist backend\requirements_qwen.txt (echo [FAIL] requirements_qwen.txt still exists & set /a FAIL+=1) else (echo [PASS] requirements_qwen.txt removed & set /a PASS+=1)

echo.
echo ==========================================
echo Checking essential files still exist...
echo ==========================================
echo.

REM Check essential files
if exist backend\certisense_main.py (echo [PASS] certisense_main.py exists) else (echo [FAIL] certisense_main.py MISSING!)
if exist backend\auth_db.py (echo [PASS] auth_db.py exists) else (echo [FAIL] auth_db.py MISSING!)
if exist backend\database.py (echo [PASS] database.py exists) else (echo [FAIL] database.py MISSING!)
if exist backend\models.py (echo [PASS] models.py exists) else (echo [FAIL] models.py MISSING!)
if exist backend\admin_api.py (echo [PASS] admin_api.py exists) else (echo [FAIL] admin_api.py MISSING!)
if exist backend\institute_routes.py (echo [PASS] institute_routes.py exists) else (echo [FAIL] institute_routes.py MISSING!)
if exist backend\student_routes.py (echo [PASS] student_routes.py exists) else (echo [FAIL] student_routes.py MISSING!)
if exist backend\verifier_routes.py (echo [PASS] verifier_routes.py exists) else (echo [FAIL] verifier_routes.py MISSING!)
if exist backend\institute_service.py (echo [PASS] institute_service.py exists) else (echo [FAIL] institute_service.py MISSING!)
if exist backend\student_service.py (echo [PASS] student_service.py exists) else (echo [FAIL] student_service.py MISSING!)
if exist backend\verifier_service.py (echo [PASS] verifier_service.py exists) else (echo [FAIL] verifier_service.py MISSING!)
if exist backend\blockchain_service.py (echo [PASS] blockchain_service.py exists) else (echo [FAIL] blockchain_service.py MISSING!)
if exist backend\ai_service.py (echo [PASS] ai_service.py exists) else (echo [FAIL] ai_service.py MISSING!)
if exist backend\chatbot_service.py (echo [PASS] chatbot_service.py exists) else (echo [FAIL] chatbot_service.py MISSING!)
if exist backend\requirements.txt (echo [PASS] requirements.txt exists) else (echo [FAIL] requirements.txt MISSING!)

echo.
echo ==========================================
echo Verification Summary
echo ==========================================
echo Total checks: %TOTAL%
echo Passed: %PASS%
echo Failed: %FAIL%
echo.

if %FAIL% EQU 0 (
    echo [SUCCESS] All duplicate files removed successfully!
    echo [SUCCESS] All essential files intact!
    echo.
    echo ==========================================
    echo Next Steps:
    echo ==========================================
    echo 1. Test application:
    echo    cd backend
    echo    python certisense_main.py
    echo.
    echo 2. Verify endpoints:
    echo    curl http://localhost:8000/health
    echo.
    echo 3. Run frontend:
    echo    cd frontend\web
    echo    npm run dev
    echo ==========================================
) else (
    echo [WARNING] %FAIL% file(s) still exist or missing!
    echo Please review the output above.
    echo.
    echo If duplicate files still exist, run cleanup_duplicates.bat again.
    echo If essential files are missing, restore from backup.
)

echo.
pause
