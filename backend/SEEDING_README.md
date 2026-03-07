# Database Seeding and Reset System

This directory contains utilities for populating and cleaning the CertiSense AI v3.0 database with test data.

## 📁 Files

- `seed_database.py` - Populates database with realistic test data
- `reset_database.py` - Removes all data and certificate files
- `test_database_state.py` - Displays current database state
- `SEEDING_README.md` - This documentation file

## 🚀 Quick Start

### 1. Install Dependencies

```bash
pip install faker reportlab
```

### 2. Seed Database

```bash
python seed_database.py
```

### 3. Check Results

```bash
python test_database_state.py
```

### 4. Reset Database (when needed)

```bash
python reset_database.py
```

## 📊 Generated Data

### Institutes (10-30)
- Realistic institute names (MIT Aluva, Codeless Institute, etc.)
- Complete contact information
- Unique institute IDs (INST00001, INST00002, etc.)

### Students (50-150 per institute)
- Student IDs following format: INST00001-00001
- Realistic names and contact information
- Various programs and departments
- Linked to institutes

### Certificates (1-3 per student)
- PDF certificates generated with ReportLab
- SHA256 hashes calculated from PDF content
- Realistic certificate content and formatting
- Stored in `uploads/certificates/`
- Various certificate types and statuses

### Verifiers (20)
- Different verifier types (employer, organization, recruiter)
- Realistic company names
- Complete profile information

### Verifications (0-5 per certificate)
- Random verification results
- Confidence scores
- Blockchain integrity flags
- Timestamps and status tracking

## 🔧 Script Details

### seed_database.py

**Purpose**: Populate database with large-scale test data

**Features**:
- Generates realistic PDF certificates using ReportLab
- Calculates proper SHA256 hashes
- Creates hierarchical data relationships
- Maintains referential integrity
- Provides progress feedback

**Output Example**:
```
🌱 Starting database seeding process...
==================================================
✓ Created 25 institutes
✓ Created 2,847 students across all institutes
✓ Created 4,921 certificates with PDF files
✓ Created 20 verifiers
✓ Created 1,234 verification records
✓ Created 18 feedback entries
==================================================
🎉 Seed Complete
Institutes created: 25
Students created: 2,847
Certificates created: 4,921
Verifiers created: 20
Verifications created: 1,234
PDF files generated: 4,921
==================================================
```

### reset_database.py

**Purpose**: Clean database and certificate files

**Safety Features**:
- Requires explicit "YES" confirmation
- Shows current data counts before deletion
- Deletes in correct dependency order
- Verifies cleanup completion

**Process**:
1. Counts existing records
2. Requests user confirmation
3. Deletes database records (proper order)
4. Removes certificate PDF files
5. Resets auto-increment sequences
6. Verifies cleanup completion

### test_database_state.py

**Purpose**: Display current database state

**Information Shown**:
- Record counts for all tables
- PDF file count
- Sample data from each table
- Database readiness status

## 📋 Data Relationships

```
Institute (1) → Students (many)
Institute (1) → Certificates (many)
Student (1) → Certificates (many)
Certificate (1) → Verifications (many)
Verifier (1) → Verifications (many)
Verifier (1) → Feedback (many)
```

## 🔐 Security Considerations

- All passwords are hashed using SHA256
- No real personal data is used (Faker library)
- Certificate hashes are properly calculated
- File paths are validated

## 📈 Expected Scale

After seeding, expect approximately:
- **Institutes**: 10-30
- **Students**: 500-4,500
- **Certificates**: 500-13,500
- **Verifiers**: 20
- **Verifications**: 0-67,500
- **PDF Files**: 500-13,500

## 🛠️ Troubleshooting

### Missing Dependencies
```bash
pip install faker reportlab
```

### Permission Errors
Ensure write permissions for:
- `data/certisense.db`
- `uploads/certificates/`

### Database Locked
Close any open database connections or restart the FastAPI server.

### Large Dataset Performance
For very large datasets (>10,000 certificates), consider:
- Running seeding in smaller batches
- Monitoring disk space for PDF files
- Allowing extra time for completion

## 🔄 Workflow Examples

### Fresh Development Setup
```bash
python reset_database.py    # Clean slate
python seed_database.py     # Populate with test data
python test_database_state.py  # Verify results
```

### Testing Different Scenarios
```bash
python reset_database.py    # Clean
python seed_database.py     # Seed with random data
# Run tests
python reset_database.py    # Clean again
python seed_database.py     # Seed with different random data
```

### Production-like Testing
```bash
python seed_database.py     # Generate large dataset
# Run performance tests
# Test dashboard loading
# Test API endpoints
python reset_database.py    # Clean when done
```

## ⚠️ Important Notes

- **DO NOT** run these scripts on production databases
- **ALWAYS** backup important data before using reset script
- Certificate PDF files can consume significant disk space
- Seeding large datasets may take several minutes
- Reset operation is **irreversible**

## 🎯 Integration with CertiSense

These scripts work seamlessly with the existing CertiSense system:
- All generated data follows existing schema
- Certificate hashes match verification system logic
- Student IDs follow the established format
- API endpoints work normally with seeded data
- Dashboards display seeded data correctly

The seeded data provides a realistic testing environment for:
- Dashboard analytics
- Certificate verification workflows
- User authentication testing
- Performance optimization
- UI/UX testing with realistic data volumes