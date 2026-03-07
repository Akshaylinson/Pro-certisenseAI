import os
import uuid
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from sqlalchemy import func

from database import Institute, Student, Certificate, Verifier, Verification, CertificateStatusEnum

class ReportVisualizer:
    def __init__(self):
        self.output_dir = "uploads/reports"
        os.makedirs(self.output_dir, exist_ok=True)
        
        # Set style
        plt.style.use('default')
        plt.rcParams['figure.figsize'] = (10, 6)
        plt.rcParams['font.size'] = 10
    
    def create_institute_chart(self, db: Session) -> str:
        """Create institute performance chart"""
        # Get top 10 institutes by certificate count
        institutes_data = db.query(
            Institute.name,
            func.count(Certificate.id).label('cert_count')
        ).join(Certificate, Institute.id == Certificate.institute_id)\
         .group_by(Institute.id)\
         .order_by(func.count(Certificate.id).desc())\
         .limit(10).all()
        
        if not institutes_data:
            return self._create_no_data_chart("Institute Performance")
        
        names = [inst[0][:20] + "..." if len(inst[0]) > 20 else inst[0] for inst in institutes_data]
        counts = [inst[1] for inst in institutes_data]
        
        fig, ax = plt.subplots()
        bars = ax.bar(range(len(names)), counts, color='#2E86AB')
        
        ax.set_xlabel('Institutes')
        ax.set_ylabel('Certificate Count')
        ax.set_title(f'Top Institute Performance\nGenerated: {datetime.now().strftime("%Y-%m-%d %H:%M")}')
        ax.set_xticks(range(len(names)))
        ax.set_xticklabels(names, rotation=45, ha='right')
        
        # Add value labels on bars
        for bar, count in zip(bars, counts):
            ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.5,
                   str(count), ha='center', va='bottom')
        
        plt.tight_layout()
        filename = f"institute_report_{uuid.uuid4().hex[:8]}.png"
        filepath = os.path.join(self.output_dir, filename)
        plt.savefig(filepath, dpi=150, bbox_inches='tight')
        plt.close()
        
        return f"/uploads/reports/{filename}"
    
    def create_certificate_chart(self, db: Session) -> str:
        """Create certificate status distribution chart"""
        active_count = db.query(Certificate).filter(Certificate.status == CertificateStatusEnum.ACTIVE).count()
        revoked_count = db.query(Certificate).filter(Certificate.status == CertificateStatusEnum.REVOKED).count()
        suspicious_count = db.query(Certificate).filter(Certificate.status == CertificateStatusEnum.SUSPICIOUS).count()
        
        if active_count == 0 and revoked_count == 0 and suspicious_count == 0:
            return self._create_no_data_chart("Certificate Status Distribution")
        
        labels = []
        sizes = []
        colors = []
        
        if active_count > 0:
            labels.append(f'Active ({active_count})')
            sizes.append(active_count)
            colors.append('#28A745')
        
        if revoked_count > 0:
            labels.append(f'Revoked ({revoked_count})')
            sizes.append(revoked_count)
            colors.append('#DC3545')
        
        if suspicious_count > 0:
            labels.append(f'Suspicious ({suspicious_count})')
            sizes.append(suspicious_count)
            colors.append('#FFC107')
        
        fig, ax = plt.subplots()
        wedges, texts, autotexts = ax.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90)
        
        ax.set_title(f'Certificate Status Distribution\nGenerated: {datetime.now().strftime("%Y-%m-%d %H:%M")}')
        
        plt.tight_layout()
        filename = f"certificate_report_{uuid.uuid4().hex[:8]}.png"
        filepath = os.path.join(self.output_dir, filename)
        plt.savefig(filepath, dpi=150, bbox_inches='tight')
        plt.close()
        
        return f"/uploads/reports/{filename}"
    
    def create_verification_chart(self, db: Session) -> str:
        """Create verification success rate chart"""
        valid_count = db.query(Verification).filter(Verification.result == True).count()
        invalid_count = db.query(Verification).filter(Verification.result == False).count()
        
        if valid_count == 0 and invalid_count == 0:
            return self._create_no_data_chart("Verification Results")
        
        labels = ['Valid', 'Invalid']
        sizes = [valid_count, invalid_count]
        colors = ['#28A745', '#DC3545']
        
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 6))
        
        # Pie chart
        wedges, texts, autotexts = ax1.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90)
        ax1.set_title('Verification Results Distribution')
        
        # Bar chart for last 7 days
        daily_data = []
        for i in range(7):
            date = datetime.utcnow() - timedelta(days=i)
            day_start = date.replace(hour=0, minute=0, second=0, microsecond=0)
            day_end = day_start + timedelta(days=1)
            
            daily_verifs = db.query(Verification).filter(
                Verification.timestamp >= day_start,
                Verification.timestamp < day_end
            ).count()
            
            daily_data.append((date.strftime("%m-%d"), daily_verifs))
        
        daily_data.reverse()  # Show oldest to newest
        dates = [item[0] for item in daily_data]
        counts = [item[1] for item in daily_data]
        
        ax2.plot(dates, counts, marker='o', color='#2E86AB', linewidth=2)
        ax2.set_xlabel('Date')
        ax2.set_ylabel('Verification Count')
        ax2.set_title('Daily Verification Trend (Last 7 Days)')
        ax2.grid(True, alpha=0.3)
        
        plt.suptitle(f'Verification Analysis\nGenerated: {datetime.now().strftime("%Y-%m-%d %H:%M")}')
        plt.tight_layout()
        
        filename = f"verification_report_{uuid.uuid4().hex[:8]}.png"
        filepath = os.path.join(self.output_dir, filename)
        plt.savefig(filepath, dpi=150, bbox_inches='tight')
        plt.close()
        
        return f"/uploads/reports/{filename}"
    
    def create_system_chart(self, db: Session) -> str:
        """Create system overview chart"""
        total_institutes = db.query(Institute).count()
        total_students = db.query(Student).count()
        total_certificates = db.query(Certificate).count()
        total_verifiers = db.query(Verifier).count()
        total_verifications = db.query(Verification).count()
        
        if all(count == 0 for count in [total_institutes, total_students, total_certificates, total_verifiers, total_verifications]):
            return self._create_no_data_chart("System Overview")
        
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(12, 10))
        
        # System entities overview
        entities = ['Institutes', 'Students', 'Certificates', 'Verifiers', 'Verifications']
        counts = [total_institutes, total_students, total_certificates, total_verifiers, total_verifications]
        colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7']
        
        bars = ax1.bar(entities, counts, color=colors)
        ax1.set_title('System Entities Overview')
        ax1.set_ylabel('Count')
        
        # Add value labels on bars
        for bar, count in zip(bars, counts):
            ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height() + max(counts) * 0.01,
                    str(count), ha='center', va='bottom')
        
        # Certificate status pie chart
        active_count = db.query(Certificate).filter(Certificate.status == CertificateStatusEnum.ACTIVE).count()
        revoked_count = db.query(Certificate).filter(Certificate.status == CertificateStatusEnum.REVOKED).count()
        
        if active_count > 0 or revoked_count > 0:
            cert_labels = ['Active', 'Revoked']
            cert_sizes = [active_count, revoked_count]
            cert_colors = ['#28A745', '#DC3545']
            ax2.pie(cert_sizes, labels=cert_labels, colors=cert_colors, autopct='%1.1f%%')
            ax2.set_title('Certificate Status')
        else:
            ax2.text(0.5, 0.5, 'No Certificate Data', ha='center', va='center', transform=ax2.transAxes)
            ax2.set_title('Certificate Status')
        
        # Daily activity trend
        daily_activity = []
        for i in range(7):
            date = datetime.utcnow() - timedelta(days=i)
            day_start = date.replace(hour=0, minute=0, second=0, microsecond=0)
            day_end = day_start + timedelta(days=1)
            
            daily_certs = db.query(Certificate).filter(
                Certificate.created_at >= day_start,
                Certificate.created_at < day_end
            ).count()
            
            daily_activity.append((date.strftime("%m-%d"), daily_certs))
        
        daily_activity.reverse()
        dates = [item[0] for item in daily_activity]
        cert_counts = [item[1] for item in daily_activity]
        
        ax3.plot(dates, cert_counts, marker='o', color='#45B7D1', linewidth=2, label='Certificates')
        ax3.set_xlabel('Date')
        ax3.set_ylabel('Count')
        ax3.set_title('Daily Certificate Issuance (Last 7 Days)')
        ax3.grid(True, alpha=0.3)
        ax3.legend()
        
        # Success rate gauge (simplified as bar)
        success_rate = 0
        if total_verifications > 0:
            valid_verifs = db.query(Verification).filter(Verification.result == True).count()
            success_rate = (valid_verifs / total_verifications) * 100
        
        ax4.bar(['Success Rate'], [success_rate], color='#28A745' if success_rate > 80 else '#FFC107' if success_rate > 60 else '#DC3545')
        ax4.set_ylim(0, 100)
        ax4.set_ylabel('Percentage')
        ax4.set_title('Verification Success Rate')
        ax4.text(0, success_rate + 2, f'{success_rate:.1f}%', ha='center', va='bottom')
        
        plt.suptitle(f'System Overview Dashboard\nGenerated: {datetime.now().strftime("%Y-%m-%d %H:%M")}')
        plt.tight_layout()
        
        filename = f"system_report_{uuid.uuid4().hex[:8]}.png"
        filepath = os.path.join(self.output_dir, filename)
        plt.savefig(filepath, dpi=150, bbox_inches='tight')
        plt.close()
        
        return f"/uploads/reports/{filename}"
    
    def _create_no_data_chart(self, title: str) -> str:
        """Create a chart indicating no data available"""
        fig, ax = plt.subplots()
        ax.text(0.5, 0.5, 'No Data Available', ha='center', va='center', 
                transform=ax.transAxes, fontsize=16, color='gray')
        ax.set_title(f'{title}\nGenerated: {datetime.now().strftime("%Y-%m-%d %H:%M")}')
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        ax.axis('off')
        
        filename = f"no_data_{uuid.uuid4().hex[:8]}.png"
        filepath = os.path.join(self.output_dir, filename)
        plt.savefig(filepath, dpi=150, bbox_inches='tight')
        plt.close()
        
        return f"/uploads/reports/{filename}"