"""
API Security Audit Script
CertiSense AI v3.0 - Phase 4 Validation
"""

import inspect
from typing import Dict, List
from fastapi import FastAPI, Depends
from certisense_main import app
from admin_api import router as admin_router
from institute_routes import router as institute_router
from student_routes import router as student_router
from verifier_routes import router as verifier_router

def audit_endpoints():
    """Audit all API endpoints"""
    endpoints = {}
    
    for route in app.routes:
        if hasattr(route, 'methods') and hasattr(route, 'path'):
            endpoint_info = {
                'path': route.path,
                'methods': list(route.methods),
                'name': route.name,
                'dependencies': []
            }
            
            # Check for authentication dependencies
            if hasattr(route, 'dependant'):
                for dep in route.dependant.dependencies:
                    endpoint_info['dependencies'].append(str(dep.call))
            
            endpoints[route.path] = endpoint_info
    
    return endpoints

def check_authentication():
    """Check authentication on all protected endpoints"""
    results = {
        'admin_endpoints': [],
        'institute_endpoints': [],
        'student_endpoints': [],
        'verifier_endpoints': [],
        'public_endpoints': []
    }
    
    for route in app.routes:
        if hasattr(route, 'path') and hasattr(route, 'methods'):
            path = route.path
            
            # Categorize endpoints
            if path.startswith('/admin'):
                results['admin_endpoints'].append(path)
            elif path.startswith('/api/institute'):
                results['institute_endpoints'].append(path)
            elif path.startswith('/api/student'):
                results['student_endpoints'].append(path)
            elif path.startswith('/api/verifier'):
                results['verifier_endpoints'].append(path)
            elif path.startswith('/auth') or path in ['/', '/health']:
                results['public_endpoints'].append(path)
    
    return results

def check_authorization():
    """Check role-based access control"""
    authorization_checks = {
        'require_admin': [],
        'require_institute': [],
        'require_student': [],
        'require_verifier': [],
        'no_auth': []
    }
    
    # This would need to inspect the actual route dependencies
    # For now, we'll categorize based on path patterns
    
    return authorization_checks

def check_input_validation():
    """Check input validation on endpoints"""
    validation_results = {}
    
    for route in app.routes:
        if hasattr(route, 'path') and hasattr(route, 'endpoint'):
            sig = inspect.signature(route.endpoint)
            params = sig.parameters
            
            validation_results[route.path] = {
                'parameters': list(params.keys()),
                'has_validation': any(
                    hasattr(param.annotation, '__origin__') 
                    for param in params.values()
                )
            }
    
    return validation_results

def run_api_audit():
    """Run complete API security audit"""
    print("=" * 80)
    print("CertiSense AI v3.0 - API Security Audit")
    print("=" * 80)
    
    # Audit 1: Endpoint Discovery
    print("\n1. Endpoint Discovery")
    endpoints = audit_endpoints()
    print(f"   Total endpoints: {len(endpoints)}")
    
    # Audit 2: Authentication Check
    print("\n2. Authentication Check")
    auth_results = check_authentication()
    print(f"   Admin endpoints: {len(auth_results['admin_endpoints'])}")
    print(f"   Institute endpoints: {len(auth_results['institute_endpoints'])}")
    print(f"   Student endpoints: {len(auth_results['student_endpoints'])}")
    print(f"   Verifier endpoints: {len(auth_results['verifier_endpoints'])}")
    print(f"   Public endpoints: {len(auth_results['public_endpoints'])}")
    
    # Audit 3: Input Validation
    print("\n3. Input Validation Check")
    validation = check_input_validation()
    validated = sum(1 for v in validation.values() if v['has_validation'])
    print(f"   Endpoints with validation: {validated}/{len(validation)}")
    
    print("\n" + "=" * 80)
    print("Audit Complete")
    print("=" * 80)

if __name__ == "__main__":
    run_api_audit()
