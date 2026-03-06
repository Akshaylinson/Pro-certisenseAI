import React from 'react';
import { AuthProvider, useAuth } from './contexts/AuthContext';
import LoginForm from './components/LoginForm';
import AdminDashboard from './components/AdminDashboard';
import InstituteDashboard from './components/InstituteDashboard';
import StudentDashboard from './components/StudentDashboard';
import VerifierDashboard from './components/VerifierDashboard';

function AppContent() {
  const { isAuthenticated, isAdmin, isInstitute, isStudent, isVerifier } = useAuth();

  if (!isAuthenticated) {
    return <LoginForm />;
  }

  if (isAdmin) {
    return <AdminDashboard />;
  }

  if (isInstitute) {
    return <InstituteDashboard />;
  }

  if (isStudent) {
    return <StudentDashboard />;
  }

  if (isVerifier) {
    return <VerifierDashboard />;
  }

  return <LoginForm />;
}

export default function App() {
  return (
    <AuthProvider>
      <AppContent />
    </AuthProvider>
  );
}