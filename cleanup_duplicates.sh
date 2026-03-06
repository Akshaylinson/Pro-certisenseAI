#!/bin/bash
# CertiSense AI v3.0 - Duplicate File Cleanup Script
# Phase 5 - System Cleanup

echo "=========================================="
echo "CertiSense AI v3.0 - Duplicate File Cleanup"
echo "=========================================="
echo ""

# Create backup
BACKUP_DIR="../backup_$(date +%Y%m%d_%H%M%S)"
echo "Creating backup at: $BACKUP_DIR"
mkdir -p "$BACKUP_DIR"
cp -r backend "$BACKUP_DIR/"
echo "✓ Backup created"
echo ""

# Remove duplicate main files
echo "Removing duplicate main files..."
rm -f backend/main.py && echo "  ✓ Removed main.py"
rm -f backend/server.py && echo "  ✓ Removed server.py"
rm -f backend/admin_main.py && echo "  ✓ Removed admin_main.py"
rm -f backend/verifier_main.py && echo "  ✓ Removed verifier_main.py"
rm -f backend/working_main.py && echo "  ✓ Removed working_main.py"
rm -f backend/certisense_minimal.py && echo "  ✓ Removed certisense_minimal.py"
rm -f backend/app/main.py && echo "  ✓ Removed app/main.py"
echo ""

# Remove duplicate auth files
echo "Removing duplicate auth files..."
rm -f backend/auth.py && echo "  ✓ Removed auth.py"
rm -f backend/verifier_auth.py && echo "  ✓ Removed verifier_auth.py"
echo ""

# Remove duplicate model files
echo "Removing duplicate model files..."
rm -f backend/verifier_models.py && echo "  ✓ Removed verifier_models.py"
rm -f backend/app/models/schemas.py && echo "  ✓ Removed app/models/schemas.py"
echo ""

# Remove duplicate API files
echo "Removing duplicate API files..."
rm -f backend/verifier_api.py && echo "  ✓ Removed verifier_api.py"
echo ""

# Remove unused utility files
echo "Removing unused utility files..."
rm -f backend/storage.py && echo "  ✓ Removed storage.py"
rm -f backend/simple_test.py && echo "  ✓ Removed simple_test.py"
rm -f backend/app/contract_client.py && echo "  ✓ Removed app/contract_client.py"
rm -f backend/app/hash_util.py && echo "  ✓ Removed app/hash_util.py"
rm -f backend/app/verification_utils.py && echo "  ✓ Removed app/verification_utils.py"
echo ""

# Archive migration files
echo "Archiving migration files..."
ARCHIVE_DIR="../archive"
mkdir -p "$ARCHIVE_DIR"
mv backend/verifier_migration.py "$ARCHIVE_DIR/" 2>/dev/null && echo "  ✓ Archived verifier_migration.py"
echo ""

# Remove duplicate requirements
echo "Removing duplicate requirements..."
rm -f backend/requirements_fixed.txt && echo "  ✓ Removed requirements_fixed.txt"
rm -f backend/requirements_minimal.txt && echo "  ✓ Removed requirements_minimal.txt"
rm -f backend/requirements_qwen.txt && echo "  ✓ Removed requirements_qwen.txt"
echo ""

echo "=========================================="
echo "Cleanup Summary"
echo "=========================================="
echo "✓ Duplicate main files removed: 7"
echo "✓ Duplicate auth files removed: 2"
echo "✓ Duplicate model files removed: 2"
echo "✓ Duplicate API files removed: 1"
echo "✓ Unused utility files removed: 5"
echo "✓ Duplicate requirements removed: 3"
echo "✓ Migration files archived: 1"
echo ""
echo "Total files removed: 20+"
echo "Backup location: $BACKUP_DIR"
echo ""
echo "=========================================="
echo "Next Steps:"
echo "=========================================="
echo "1. Test application: cd backend && python certisense_main.py"
echo "2. Verify endpoints: curl http://localhost:8000/health"
echo "3. Run frontend: cd frontend/web && npm run dev"
echo ""
echo "If issues occur, restore from: $BACKUP_DIR"
echo "=========================================="
