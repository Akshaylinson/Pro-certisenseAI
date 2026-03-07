#!/usr/bin/env python3
"""
Test script for AI-powered report generation system
"""

import sys
import os

# Add the backend directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from database import SessionLocal
from report_service import ReportService

def test_report_generation():
    """Test all report generation functions"""
    print("Testing AI-Powered Report Generation System")
    print("=" * 50)
    
    db = SessionLocal()
    report_service = ReportService()
    
    try:
        # Test Institute Report
        print("1. Testing Institute Report...")
        institute_report = report_service.generate_institute_report(db)
        print(f"   Generated institute report with {len(institute_report['metrics'])} metrics")
        print(f"   AI Summary: {institute_report['ai_summary'][:100]}...")
        print(f"   Chart URL: {institute_report['chart_url']}")
        
        # Test Certificate Report
        print("\n2. Testing Certificate Report...")
        certificate_report = report_service.generate_certificate_report(db)
        print(f"   Generated certificate report with {len(certificate_report['metrics'])} metrics")
        print(f"   AI Summary: {certificate_report['ai_summary'][:100]}...")
        print(f"   Chart URL: {certificate_report['chart_url']}")
        
        # Test Verification Report
        print("\n3. Testing Verification Report...")
        verification_report = report_service.generate_verification_report(db)
        print(f"   Generated verification report with {len(verification_report['metrics'])} metrics")
        print(f"   AI Summary: {verification_report['ai_summary'][:100]}...")
        print(f"   Chart URL: {verification_report['chart_url']}")
        
        # Test System Report
        print("\n4. Testing System Report...")
        system_report = report_service.generate_system_report(db)
        print(f"   Generated system report with {len(system_report['metrics'])} metrics")
        print(f"   AI Summary: {system_report['ai_summary'][:100]}...")
        print(f"   Chart URL: {system_report['chart_url']}")
        
        print("\n" + "=" * 50)
        print("All report generation tests passed!")
        print("AI summaries generated successfully")
        print("Charts created and saved")
        print("Report system is ready for use")
        
        # Display sample metrics
        print("\nSample Metrics from System Report:")
        for key, value in system_report['metrics'].items():
            if key != 'daily_activity_trend':
                print(f"   {key}: {value}")
        
    except Exception as e:
        print(f"Error during testing: {str(e)}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()

def test_chart_generation():
    """Test chart generation specifically"""
    print("\nTesting Chart Generation...")
    
    try:
        from report_visualizer import ReportVisualizer
        db = SessionLocal()
        visualizer = ReportVisualizer()
        
        # Test each chart type
        institute_chart = visualizer.create_institute_chart(db)
        print(f"   Institute chart: {institute_chart}")
        
        certificate_chart = visualizer.create_certificate_chart(db)
        print(f"   Certificate chart: {certificate_chart}")
        
        verification_chart = visualizer.create_verification_chart(db)
        print(f"   Verification chart: {verification_chart}")
        
        system_chart = visualizer.create_system_chart(db)
        print(f"   System chart: {system_chart}")
        
        print("   All charts generated successfully!")
        
        db.close()
        
    except Exception as e:
        print(f"   Chart generation error: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_report_generation()
    test_chart_generation()
    print("\nReport generation system testing complete!")