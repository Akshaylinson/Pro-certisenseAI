"""
Migration + Seed script for CertiSense DB.
Run from project root: python migrate_and_seed.py
"""
import sqlite3
import uuid
import hashlib
from datetime import datetime

DB_PATH = "data/certisense.db"

def hash_password(p):
    return hashlib.sha256(p.encode()).hexdigest()

conn = sqlite3.connect(DB_PATH)
cur = conn.cursor()

# ── 1. Fix institutes table: ensure institute_id column is correct ──────────
cur.execute("PRAGMA table_info(institutes)")
inst_cols = [r[1] for r in cur.fetchall()]
print("Institutes cols:", inst_cols)

# The old row has institute_id stored in col index 7 (value 'INTT00001')
# SQLAlchemy model expects institute_id as a unique indexed column — it's there.
# Just verify the existing institute row is usable.
cur.execute("SELECT id, name, institute_id, email, password_hash FROM institutes")
institutes = cur.fetchall()
print("Existing institutes:", institutes)

if not institutes:
    print("No institutes found — inserting default")
    inst_id = str(uuid.uuid4())
    cur.execute("""
        INSERT INTO institutes (id, name, institute_id, email, password_hash, location, approval_status, is_verified, created_at)
        VALUES (?, ?, ?, ?, ?, ?, 'approved', 1, ?)
    """, (inst_id, "St. Annes", "INST00001", "stannes@gg.in", hash_password("institute123"), "Thrissur", datetime.utcnow()))
    conn.commit()
    cur.execute("SELECT id, name, institute_id, email, password_hash FROM institutes")
    institutes = cur.fetchall()

institute_db_id = institutes[0][0]
institute_id_code = institutes[0][2]
print(f"Using institute: id={institute_db_id}, code={institute_id_code}")

# ── 2. Seed students ─────────────────────────────────────────────────────────
cur.execute("SELECT COUNT(*) FROM students")
student_count = cur.fetchone()[0]

if student_count == 0:
    print("Seeding students...")
    students_data = [
        ("Alice Johnson", "alice@student.com", "alice123"),
        ("Bob Smith",     "bob@student.com",   "bob123"),
        ("Carol White",   "carol@student.com", "carol123"),
    ]
    student_ids = []
    for i, (name, email, pwd) in enumerate(students_data, 1):
        sid = str(uuid.uuid4())
        student_code = f"{institute_id_code}-{str(i).zfill(5)}"
        cur.execute("""
            INSERT INTO students (id, student_id, name, email, password_hash, institute_id, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (sid, student_code, name, email, hash_password(pwd), institute_db_id, datetime.utcnow()))
        student_ids.append((sid, student_code, name))
        print(f"  Added student: {student_code} / {name}")
    conn.commit()
else:
    cur.execute("SELECT id, student_id, name FROM students WHERE institute_id=?", (institute_db_id,))
    student_ids = cur.fetchall()
    print(f"Students already exist: {student_ids}")

# ── 3. Seed certificates ─────────────────────────────────────────────────────
cur.execute("SELECT COUNT(*) FROM certificates")
cert_count = cur.fetchone()[0]

if cert_count == 0:
    print("Seeding certificates...")
    cert_names = ["Bachelor of Computer Science", "Python Programming", "Data Science Fundamentals"]
    for i, (s_id, s_code, s_name) in enumerate(student_ids):
        cert_id = str(uuid.uuid4())
        cert_hash = hashlib.sha256(f"{s_code}-{cert_names[i]}".encode()).hexdigest()
        chain_hash = hashlib.sha256(f"chain-{cert_hash}".encode()).hexdigest()
        cur.execute("""
            INSERT INTO certificates (id, name, hash, chain_hash, student_id, institute_id, issuer_id,
                certificate_type, status, issue_date, verification_count, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (cert_id, cert_names[i], cert_hash, chain_hash, s_id, institute_db_id, institute_db_id,
              "degree", "ACTIVE", datetime.utcnow(), 0, datetime.utcnow()))
        print(f"  Added cert: {cert_names[i]} for {s_name}")
    conn.commit()
else:
    print(f"Certificates already exist: {cert_count}")

# ── 4. Summary ───────────────────────────────────────────────────────────────
cur.execute("SELECT COUNT(*) FROM institutes"); print(f"\nFinal counts — Institutes: {cur.fetchone()[0]}")
cur.execute("SELECT COUNT(*) FROM students");  print(f"Students: {cur.fetchone()[0]}")
cur.execute("SELECT COUNT(*) FROM certificates"); print(f"Certificates: {cur.fetchone()[0]}")

conn.close()
print("\nDone. Restart docker-compose to pick up changes.")
print(f"\nInstitute login: email=stannes@gg.in  (use the password you registered with)")
print("Student logins:")
for _, code, name in student_ids:
    print(f"  {code} / (password set during seeding)")
