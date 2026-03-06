"""
CertiSense AI v3.0 - Cleanup Verification Script (Python)
Verifies that duplicate files were successfully removed and essential files remain
"""

import os
import sys
from pathlib import Path

class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    END = '\033[0m'

def check_file_removed(filepath):
    """Check if a file was successfully removed"""
    if os.path.exists(filepath):
        return False, f"[FAIL] {filepath} still exists"
    return True, f"[PASS] {filepath} removed"

def check_file_exists(filepath):
    """Check if an essential file still exists"""
    if os.path.exists(filepath):
        return True, f"[PASS] {filepath} exists"
    return False, f"[FAIL] {filepath} MISSING!"

def main():
    print("=" * 60)
    print("CertiSense AI v3.0 - Cleanup Verification")
    print("=" * 60)
    print()

    base_dir = Path("backend")
    passed = 0
    failed = 0
    total = 0

    # Files that should be removed
    removed_files = [
        # Duplicate main files
        "main.py",
        "server.py",
        "admin_main.py",
        "verifier_main.py",
        "working_main.py",
        "certisense_minimal.py",
        "app/main.py",
        # Duplicate auth files
        "auth.py",
        "verifier_auth.py",
        # Duplicate model files
        "verifier_models.py",
        "app/models/schemas.py",
        # Duplicate API files
        "verifier_api.py",
        # Unused utility files
        "storage.py",
        "simple_test.py",
        "app/contract_client.py",
        "app/hash_util.py",
        "app/verification_utils.py",
        # Duplicate requirements
        "requirements_fixed.txt",
        "requirements_minimal.txt",
        "requirements_qwen.txt",
    ]

    # Essential files that must exist
    essential_files = [
        "certisense_main.py",
        "auth_db.py",
        "database.py",
        "models.py",
        "admin_api.py",
        "institute_routes.py",
        "student_routes.py",
        "verifier_routes.py",
        "institute_service.py",
        "student_service.py",
        "verifier_service.py",
        "blockchain_service.py",
        "ai_service.py",
        "chatbot_service.py",
        "requirements.txt",
    ]

    print("Checking duplicate files were removed...")
    print()
    
    for file in removed_files:
        total += 1
        filepath = base_dir / file
        success, message = check_file_removed(filepath)
        if success:
            print(f"{Colors.GREEN}{message}{Colors.END}")
            passed += 1
        else:
            print(f"{Colors.RED}{message}{Colors.END}")
            failed += 1

    print()
    print("=" * 60)
    print("Checking essential files still exist...")
    print("=" * 60)
    print()

    essential_missing = 0
    for file in essential_files:
        filepath = base_dir / file
        success, message = check_file_exists(filepath)
        if success:
            print(f"{Colors.GREEN}{message}{Colors.END}")
        else:
            print(f"{Colors.RED}{message}{Colors.END}")
            essential_missing += 1

    print()
    print("=" * 60)
    print("Verification Summary")
    print("=" * 60)
    print(f"Total duplicate file checks: {total}")
    print(f"Passed: {Colors.GREEN}{passed}{Colors.END}")
    print(f"Failed: {Colors.RED}{failed}{Colors.END}")
    print(f"Essential files missing: {Colors.RED}{essential_missing}{Colors.END}")
    print()

    if failed == 0 and essential_missing == 0:
        print(f"{Colors.GREEN}[SUCCESS] All duplicate files removed successfully!{Colors.END}")
        print(f"{Colors.GREEN}[SUCCESS] All essential files intact!{Colors.END}")
        print()
        print("=" * 60)
        print("Next Steps:")
        print("=" * 60)
        print("1. Test application:")
        print("   cd backend")
        print("   python certisense_main.py")
        print()
        print("2. Verify endpoints:")
        print("   curl http://localhost:8000/health")
        print()
        print("3. Run frontend:")
        print("   cd frontend/web")
        print("   npm run dev")
        print("=" * 60)
        return 0
    else:
        print(f"{Colors.YELLOW}[WARNING] Issues detected!{Colors.END}")
        if failed > 0:
            print(f"  - {failed} duplicate file(s) still exist")
            print("  - Run cleanup_duplicates.bat again")
        if essential_missing > 0:
            print(f"  - {essential_missing} essential file(s) missing")
            print("  - Restore from backup immediately!")
        print()
        return 1

if __name__ == "__main__":
    sys.exit(main())
