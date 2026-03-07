#!/usr/bin/env python3
"""
Database Seeding Script for CertiSense AI v3.0
Populates the database with realistic test data including certificate PDFs and hashes.
"""

import os
import sys
import uuid
import hashlib
import random
from datetime import datetime, timedelta
from faker import Faker
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.platypus import Table, TableStyle

# Add the backend directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from database import SessionLocal, Institute, Student, Certificate, Verifier, Verification, Feedback
from database import CertificateStatusEnum, VerificationStatusEnum

# Initialize Faker
fake = Faker()

class DatabaseSeeder:
    def __init__(self):
        self.db = SessionLocal()
        self.institutes = []
        self.students = []
        self.certificates = []
        self.verifiers = []
        self.verifications = []
        
        # Ensure uploads directory exists
        os.makedirs("uploads/certificates", exist_ok=True)
        
        # Statistics
        self.stats = {
            'institutes': 0,
            'students': 0,
            'certificates': 0,
            'verifiers': 0,
            'verifications': 0,
            'pdfs': 0
        }

    def generate_institute_id(self, index):
        """Generate institute ID in format INST00001"""
        return f"INST{index:05d}"

    def generate_student_id(self, institute_index, student_index):
        """Generate student ID in format INST00001-00001"""
        return f"INST{institute_index:05d}-{student_index:05d}"

    def create_certificate_pdf(self, student_name, institute_name, certificate_id, issue_date, certificate_type="Certificate of Completion"):
        """Generate a realistic certificate PDF"""
        filename = f"CERT-{uuid.uuid4().hex[:12].upper()}.pdf"
        filepath = os.path.join("uploads/certificates", filename)
        
        # Create PDF document
        doc = SimpleDocTemplate(filepath, pagesize=A4)
        styles = getSampleStyleSheet()
        story = []
        
        # Title style
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=24,
            spaceAfter=30,
            alignment=1,  # Center alignment
            textColor=colors.darkblue
        )
        
        # Header style
        header_style = ParagraphStyle(
            'CustomHeader',
            parent=styles['Heading2'],
            fontSize=18,
            spaceAfter=20,
            alignment=1,
            textColor=colors.darkgreen
        )
        
        # Body style
        body_style = ParagraphStyle(
            'CustomBody',
            parent=styles['Normal'],
            fontSize=12,
            spaceAfter=12,
            alignment=1
        )
        
        # Certificate content
        story.append(Spacer(1, 0.5*inch))
        story.append(Paragraph(certificate_type, title_style))
        story.append(Spacer(1, 0.3*inch))
        
        story.append(Paragraph("This is to certify that", body_style))
        story.append(Spacer(1, 0.2*inch))
        
        story.append(Paragraph(f"<b>{student_name}</b>", header_style))
        story.append(Spacer(1, 0.2*inch))
        
        story.append(Paragraph("has successfully completed the requirements for", body_style))
        story.append(Spacer(1, 0.2*inch))
        
        course_names = [
            "Advanced Web Development",
            "Data Science and Analytics",
            "Machine Learning Fundamentals",
            "Blockchain Technology",
            "Cybersecurity Essentials",
            "Cloud Computing",
            "Mobile App Development",
            "Digital Marketing",
            "Project Management",
            "Software Engineering"
        ]
        course_name = random.choice(course_names)
        story.append(Paragraph(f"<b>{course_name}</b>", header_style))
        story.append(Spacer(1, 0.3*inch))
        
        story.append(Paragraph(f"Issued by: {institute_name}", body_style))
        story.append(Paragraph(f"Certificate ID: {certificate_id}", body_style))
        story.append(Paragraph(f"Issue Date: {issue_date.strftime('%B %d, %Y')}", body_style))
        story.append(Spacer(1, 0.5*inch))
        
        # Create a simple table for signatures
        signature_data = [
            ['_' * 30, '_' * 30],
            ['Director Signature', 'Registrar Signature'],
            [institute_name, 'Academic Office']
        ]
        
        signature_table = Table(signature_data, colWidths=[3*inch, 3*inch])
        signature_table.setStyle(TableStyle([
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ]))
        
        story.append(signature_table)
        
        # Build PDF
        doc.build(story)
        
        return filepath

    def calculate_pdf_hash(self, filepath):
        """Calculate SHA256 hash of PDF file"""
        with open(filepath, 'rb') as f:
            pdf_bytes = f.read()
            return hashlib.sha256(pdf_bytes).hexdigest()

    def seed_institutes(self):
        """Generate 10-30 institutes"""
        institute_count = random.randint(15, 20)  # Reduced range
        used_emails = set()  # Track used emails to ensure uniqueness
        
        institute_names = [
            "MIT Aluva", "Codeless Institute", "Kerala Technical College",
            "Advanced Technology Institute", "Digital Innovation Academy",
            "Future Skills University", "Tech Excellence Center",
            "Innovation Hub Institute", "Smart Learning Academy",
            "NextGen Education Center", "Elite Technical Institute",
            "Modern Skills Academy", "Progressive Learning Center",
            "Excellence Education Institute", "Premier Technology College",
            "Advanced Learning Academy", "Digital Skills Institute",
            "Technology Innovation Center", "Professional Development Academy",
            "Skill Enhancement Institute", "Career Advancement Center",
            "Technical Excellence Academy", "Modern Education Hub",
            "Innovation Learning Center", "Professional Skills Institute",
            "Advanced Career Academy", "Digital Excellence Center",
            "Future Technology Institute", "Elite Learning Academy",
            "Progressive Skills Center"
        ]
        
        for i in range(institute_count):
            institute_id = self.generate_institute_id(i + 1)
            institute_name = institute_names[i % len(institute_names)]
            if i >= len(institute_names):
                institute_name = f"{institute_name} - Branch {i - len(institute_names) + 2}"
            
            # Generate unique email
            base_email = f"admin@{institute_name.lower().replace(' ', '').replace('-', '')}.edu"
            email = base_email
            counter = 1
            while email in used_emails:
                email = f"admin{counter}@{institute_name.lower().replace(' ', '').replace('-', '')}.edu"
                counter += 1
            used_emails.add(email)
            
            institute = Institute(
                id=str(uuid.uuid4()),
                institute_id=institute_id,
                name=institute_name,
                email=email,
                password_hash=hashlib.sha256("institute123".encode()).hexdigest(),
                location=fake.city() + ", " + fake.state(),
                phone=fake.phone_number(),
                website=f"www.{institute_name.lower().replace(' ', '').replace('-', '')}.edu",
                registration_number=f"REG{random.randint(1000, 9999)}",
                approval_status="approved",
                is_verified=True,
                created_at=fake.date_time_between(start_date='-2y', end_date='now')
            )
            
            self.db.add(institute)
            self.institutes.append(institute)
            self.stats['institutes'] += 1
        
        self.db.commit()
        print("Created {} institutes".format(institute_count))

    def seed_students(self):
        """Generate 50-150 students per institute"""
        used_emails = set()  # Track used emails to ensure uniqueness
        
        for institute_index, institute in enumerate(self.institutes):
            student_count = random.randint(25, 35)  # Reduced range for ~540 total
            
            for student_index in range(student_count):
                student_id = self.generate_student_id(institute_index + 1, student_index + 1)
                
                # Generate unique email
                email = fake.email()
                while email in used_emails:
                    email = fake.email()
                used_emails.add(email)
                
                student = Student(
                    id=str(uuid.uuid4()),
                    student_id=student_id,
                    name=fake.name(),
                    email=email,
                    password_hash=hashlib.sha256("student123".encode()).hexdigest(),
                    institute_id=institute.id,
                    phone=fake.phone_number(),
                    program=random.choice([
                        "Computer Science", "Information Technology", "Data Science",
                        "Cybersecurity", "Software Engineering", "Web Development",
                        "Mobile Development", "AI & Machine Learning", "Cloud Computing"
                    ]),
                    department=random.choice([
                        "Engineering", "Computer Applications", "Information Systems",
                        "Technology", "Digital Sciences"
                    ]),
                    created_at=fake.date_time_between(start_date='-1y', end_date='now')
                )
                
                self.db.add(student)
                self.students.append(student)
                self.stats['students'] += 1
        
        self.db.commit()
        print("Created {} students across all institutes".format(self.stats['students']))

    def seed_certificates(self):
        """Generate 1-3 certificates per student"""
        for student in self.students:
            certificate_count = random.randint(1, 2)  # Reduced to 1-2 certificates per student
            
            for _ in range(certificate_count):
                certificate_id = f"CERT-{uuid.uuid4().hex[:12].upper()}"
                issue_date = fake.date_time_between(start_date='-6m', end_date='now')
                
                # Find the institute for this student
                institute = next(inst for inst in self.institutes if inst.id == student.institute_id)
                
                # Generate PDF certificate
                pdf_path = self.create_certificate_pdf(
                    student.name,
                    institute.name,
                    certificate_id,
                    issue_date
                )
                
                # Calculate hash
                certificate_hash = self.calculate_pdf_hash(pdf_path)
                
                certificate = Certificate(
                    id=str(uuid.uuid4()),
                    name=f"Certificate - {student.name}",
                    hash=certificate_hash,
                    chain_hash=hashlib.sha256(f"{certificate_hash}{issue_date}".encode()).hexdigest(),
                    student_id=student.id,
                    institute_id=student.institute_id,
                    issuer_id=institute.id,
                    certificate_type=random.choice([
                        "Course Completion", "Professional Certification", "Skill Assessment",
                        "Training Certificate", "Achievement Award"
                    ]),
                    status=random.choice([
                        CertificateStatusEnum.ACTIVE,
                        CertificateStatusEnum.ACTIVE,  # Higher probability for active
                        CertificateStatusEnum.ACTIVE,
                        CertificateStatusEnum.REVOKED
                    ]),
                    issue_date=issue_date,
                    verification_count=0,
                    created_at=issue_date
                )
                
                self.db.add(certificate)
                self.certificates.append(certificate)
                self.stats['certificates'] += 1
                self.stats['pdfs'] += 1
        
        self.db.commit()
        print("Created {} certificates with PDF files".format(self.stats['certificates']))

    def seed_verifiers(self):
        """Generate 20 verifiers"""
        verifier_count = 20
        used_emails = set()  # Track used emails to ensure uniqueness
        
        company_types = [
            "Tech Solutions", "Digital Services", "Innovation Labs", "Software Systems",
            "Data Analytics", "Cloud Services", "Consulting Group", "Technology Partners",
            "Development Studio", "IT Solutions", "Cyber Security", "AI Research",
            "Blockchain Labs", "Mobile Solutions", "Web Services", "Enterprise Solutions",
            "Startup Incubator", "Research Institute", "Training Academy", "Skill Center"
        ]
        
        verifier_types = ["employer", "organization", "recruiter"]
        
        for i in range(verifier_count):
            company_name = f"{fake.company()} {random.choice(company_types)}"
            
            # Generate unique email
            email = fake.email()
            while email in used_emails:
                email = fake.email()
            used_emails.add(email)
            
            verifier = Verifier(
                id=str(uuid.uuid4()),
                username=f"verifier_{i+1:03d}",
                email=email,
                password_hash=hashlib.sha256("verifier123".encode()).hexdigest(),
                company_name=company_name,
                verifier_type=random.choice(verifier_types),
                status="active",
                verification_count=0,
                created_at=fake.date_time_between(start_date='-1y', end_date='now')
            )
            
            self.db.add(verifier)
            self.verifiers.append(verifier)
            self.stats['verifiers'] += 1
        
        self.db.commit()
        print("Created {} verifiers".format(verifier_count))

    def seed_verifications(self):
        """Generate 0-5 verification records per certificate"""
        for certificate in self.certificates:
            verification_count = random.randint(0, 1)  # Reduced to 0-1 verifications per certificate
            
            for _ in range(verification_count):
                verifier = random.choice(self.verifiers)
                result = random.choice([True, True, True, False])  # Higher probability for valid
                
                if result:
                    status = VerificationStatusEnum.VALID
                    confidence = random.uniform(0.8, 1.0)
                else:
                    status = random.choice([
                        VerificationStatusEnum.INVALID,
                        VerificationStatusEnum.FLAGGED
                    ])
                    confidence = random.uniform(0.1, 0.6)
                
                verification = Verification(
                    id=str(uuid.uuid4()),
                    certificate_id=certificate.id,
                    certificate_hash=certificate.hash,
                    verifier_id=verifier.id,
                    result=result,
                    status=status,
                    confidence_score=confidence,
                    blockchain_integrity=result,
                    is_suspicious=not result,
                    timestamp=fake.date_time_between(
                        start_date=certificate.created_at,
                        end_date='now'
                    )
                )
                
                self.db.add(verification)
                self.verifications.append(verification)
                self.stats['verifications'] += 1
                
                # Update certificate verification count
                certificate.verification_count += 1
                
                # Update verifier verification count
                verifier.verification_count += 1
        
        self.db.commit()
        print("Created {} verification records".format(self.stats['verifications']))

    def seed_feedback(self):
        """Generate some feedback entries"""
        feedback_count = random.randint(10, 30)
        categories = ["bug_report", "feature_request", "general_feedback", "technical_issue", "improvement_suggestion"]
        
        for _ in range(feedback_count):
            verifier = random.choice(self.verifiers)
            certificate = random.choice(self.certificates) if random.choice([True, False]) else None
            
            feedback = Feedback(
                id=str(uuid.uuid4()),
                verifier_id=verifier.id,
                certificate_id=certificate.id if certificate else None,
                message=fake.text(max_nb_chars=200),
                category=random.choice(categories),
                priority=random.choice(["low", "medium", "high"]),
                status=random.choice(["open", "in_progress", "resolved"]),
                flagged=random.choice([True, False]),
                timestamp=fake.date_time_between(start_date='-3m', end_date='now')
            )
            
            self.db.add(feedback)
        
        self.db.commit()
        print("Created {} feedback entries".format(feedback_count))

    def check_existing_data(self):
        """Check if database already contains data"""
        existing_institutes = self.db.query(Institute).count()
        existing_students = self.db.query(Student).count()
        existing_certificates = self.db.query(Certificate).count()
        existing_verifiers = self.db.query(Verifier).count()
        
        total_existing = existing_institutes + existing_students + existing_certificates + existing_verifiers
        
        if total_existing > 0:
            print("Database already contains data:")
            print(f"   Institutes: {existing_institutes}")
            print(f"   Students: {existing_students}")
            print(f"   Certificates: {existing_certificates}")
            print(f"   Verifiers: {existing_verifiers}")
            print()
            print("Cannot seed database with existing data.")
            print("Please run 'python reset_database.py' first to clean the database.")
            return False
        
        return True

    def run_seed(self):
        """Execute the complete seeding process"""
        print("Starting database seeding process...")
        print("=" * 50)
        
        # Check for existing data first
        if not self.check_existing_data():
            return
        
        try:
            self.seed_institutes()
            self.seed_students()
            self.seed_certificates()
            self.seed_verifiers()
            self.seed_verifications()
            self.seed_feedback()
            
            print("=" * 50)
            print("Seed Complete")
            print(f"Institutes created: {self.stats['institutes']}")
            print(f"Students created: {self.stats['students']}")
            print(f"Certificates created: {self.stats['certificates']}")
            print(f"Verifiers created: {self.stats['verifiers']}")
            print(f"Verifications created: {self.stats['verifications']}")
            print(f"PDF files generated: {self.stats['pdfs']}")
            print("=" * 50)
            
        except Exception as e:
            print("Error during seeding: {}".format(str(e)))
            self.db.rollback()
            raise
        finally:
            self.db.close()

def main():
    """Main execution function"""
    print("CertiSense AI v3.0 - Database Seeding Script")
    print("=" * 50)
    
    # Check if required packages are installed
    try:
        import faker
        import reportlab
    except ImportError as e:
        print(f"Missing required package: {e}")
        print("Please install required packages:")
        print("pip install faker reportlab")
        return
    
    seeder = DatabaseSeeder()
    seeder.run_seed()

if __name__ == "__main__":
    main()