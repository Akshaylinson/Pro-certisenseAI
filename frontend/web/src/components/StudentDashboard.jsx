import React, { useState, useEffect } from 'react';
import { useAuth } from '../contexts/AuthContext';
import Layout from './Layout';
import { StatCard, InfoCard, Button, Badge } from './UIComponents';

const StudentDashboard = () => {
  const { user, token, logout } = useAuth();
  const [activeTab, setActiveTab] = useState('certificates');
  const [profile, setProfile] = useState(null);
  const [certificates, setCertificates] = useState([]);
  const [selectedCert, setSelectedCert] = useState(null);
  const [loading, setLoading] = useState(false);
  const [editMode, setEditMode] = useState(false);
  const [editData, setEditData] = useState({ name: '', email: '' });

  const apiCall = async (endpoint, method = 'GET', body = null) => {
    const options = {
      method,
      headers: {
        'Authorization': `Bearer ${token}`,
        ...(body && { 'Content-Type': 'application/json' })
      },
      ...(body && { body: JSON.stringify(body) })
    };

    const response = await fetch(`http://localhost:8000${endpoint}`, options);
    return response.json();
  };

  const navigationItems = [
    { id: 'profile', label: 'My Profile' },
    { id: 'certificates', label: 'My Certificates' }
  ];

  useEffect(() => {
    loadProfile();
    loadCertificates();
  }, []);

  const loadProfile = async () => {
    try {
      const data = await apiCall('/student/profile');
      setProfile(data);
      setEditData({ name: data.name, email: data.email });
    } catch (error) {
      console.error('Error loading profile:', error);
    }
  };

  const loadCertificates = async () => {
    setLoading(true);
    try {
      const data = await apiCall('/student/certificates');
      setCertificates(data.certificates || []);
    } catch (error) {
      console.error('Error loading certificates:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleProfileUpdate = async () => {
    try {
      await apiCall(`/student/profile?name=${editData.name}&email=${editData.email}`, 'PUT');
      setEditMode(false);
      loadProfile();
      alert('Profile updated successfully');
    } catch (error) {
      alert('Error updating profile');
    }
  };

  const loadCertificateDetails = async (certHash) => {
    try {
      const data = await apiCall(`/student/certificate/${certHash}`);
      setSelectedCert(data);
    } catch (error) {
      alert('Error loading certificate details');
    }
  };

  const renderProfile = () => (
    <div className="space-y-6">
      <div>
        <h2 className="text-2xl font-bold text-secondary-800">My Profile</h2>
        <p className="text-secondary-600 mt-1">View and manage your personal information</p>
      </div>
      
      {!editMode ? (
        <InfoCard title="Profile Information" icon="fa-user">
          <div className="space-y-4">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-medium text-secondary-600 mb-1">Student ID</label>
                <p className="font-mono bg-secondary-50 px-3 py-2 rounded-lg border">{profile?.student_id}</p>
              </div>
              <div>
                <label className="block text-sm font-medium text-secondary-600 mb-1">Name</label>
                <p className="px-3 py-2">{profile?.name}</p>
              </div>
              <div>
                <label className="block text-sm font-medium text-secondary-600 mb-1">Email</label>
                <p className="px-3 py-2">{profile?.email}</p>
              </div>
              <div>
                <label className="block text-sm font-medium text-secondary-600 mb-1">Joined</label>
                <p className="px-3 py-2">{new Date(profile?.created_at).toLocaleDateString()}</p>
              </div>
            </div>
            <Button onClick={() => setEditMode(true)} variant="primary" icon="fa-edit">
              Edit Profile
            </Button>
          </div>
        </InfoCard>
      ) : (
        <InfoCard title="Edit Profile">
          <div className="space-y-4">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label className="block font-medium mb-2">Name</label>
                <input
                  type="text"
                  value={editData.name}
                  onChange={(e) => setEditData({ ...editData, name: e.target.value })}
                  className="w-full"
                  placeholder="Name"
                />
              </div>
              <div>
                <label className="block font-medium mb-2">Email</label>
                <input
                  type="email"
                  value={editData.email}
                  onChange={(e) => setEditData({ ...editData, email: e.target.value })}
                  className="w-full"
                  placeholder="Email"
                />
              </div>
            </div>
            <div className="flex gap-2">
              <Button onClick={handleProfileUpdate} variant="success" icon="fa-check">
                Save Changes
              </Button>
              <Button onClick={() => setEditMode(false)} variant="secondary">
                Cancel
              </Button>
            </div>
          </div>
        </InfoCard>
      )}
    </div>
  );

  const renderCertificates = () => (
    <div className="space-y-6">
      <div>
        <h2 className="text-2xl font-bold text-secondary-800">My Certificates</h2>
        <p className="text-secondary-600 mt-1">View and manage your issued certificates</p>
      </div>
      
      {loading ? (
        <InfoCard>
          <div className="text-center py-8">
            <div className="loading-spinner mx-auto mb-4"></div>
            <p className="text-secondary-600">Loading certificates...</p>
          </div>
        </InfoCard>
      ) : certificates.length === 0 ? (
        <InfoCard>
          <div className="text-center py-12">
            <i className="fas fa-file-certificate text-6xl text-secondary-300 mb-4"></i>
            <p className="text-secondary-600 text-lg">No certificates issued yet</p>
            <p className="text-secondary-500 text-sm mt-2">Your institute will issue certificates here</p>
          </div>
        </InfoCard>
      ) : (
        <div className="space-y-4">
          {certificates.map((cert, idx) => (
            <InfoCard key={idx} className="hover:shadow-lg transition-shadow">
              <div className="flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
                <div className="flex-1 space-y-2">
                  <h3 className="font-semibold text-lg">{cert.name || `Certificate ${idx + 1}`}</h3>
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-x-4 gap-y-1 text-sm">
                    <div className="flex items-center gap-2">
                      <i className="fas fa-id-card text-secondary-400"></i>
                      <span className="text-secondary-600">ID:</span>
                      <span className="font-mono">{cert.certificate_id}</span>
                    </div>
                    <div className="flex items-center gap-2">
                      <i className="fas fa-fingerprint text-secondary-400"></i>
                      <span className="text-secondary-600">Hash:</span>
                      <span className="font-mono text-xs">{cert.hash?.substring(0, 16)}...</span>
                    </div>
                    <div className="flex items-center gap-2">
                      <i className="fas fa-calendar text-secondary-400"></i>
                      <span className="text-secondary-600">Issued:</span>
                      <span>{cert.issue_date ? new Date(cert.issue_date).toLocaleDateString() : 'N/A'}</span>
                    </div>
                    <div className="flex items-center gap-2">
                      <i className="fas fa-eye text-secondary-400"></i>
                      <span className="text-secondary-600">Verifications:</span>
                      <Badge variant="info">{cert.verification_count || 0}</Badge>
                    </div>
                  </div>
                </div>
                <div className="flex flex-col gap-2">
                  <Badge variant={cert.status === 'active' ? 'success' : 'danger'}>
                    {cert.status === 'active' ? '✓ Valid' : '✗ Revoked'}
                  </Badge>
                  <Button 
                    size="sm"
                    variant="primary" 
                    icon="fa-download"
                    onClick={(e) => {
                      e.preventDefault();
                      fetch(`http://localhost:8000/student/certificates/${cert.certificate_id}/download`, {
                        headers: { 'Authorization': `Bearer ${token}` }
                      })
                      .then(response => response.blob())
                      .then(blob => {
                        const url = window.URL.createObjectURL(blob);
                        const a = document.createElement('a');
                        a.href = url;
                        a.download = cert.name || `certificate_${cert.certificate_id}.pdf`;
                        document.body.appendChild(a);
                        a.click();
                        window.URL.revokeObjectURL(url);
                        document.body.removeChild(a);
                      })
                      .catch(err => alert('Error downloading certificate'));
                    }}
                  >
                    Download
                  </Button>
                  <Button
                    size="sm"
                    variant="secondary"
                    icon="fa-info-circle"
                    onClick={() => cert.hash && loadCertificateDetails(cert.hash)}
                  >
                    Details
                  </Button>
                </div>
              </div>
            </InfoCard>
          ))}
        </div>
      )}

      {selectedCert && (
        <InfoCard title="Certificate Details" icon="fa-file-contract">
          <div className="space-y-3">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-medium text-secondary-600 mb-1">Hash</label>
                <p className="font-mono text-xs bg-secondary-50 p-2 rounded border break-all">{selectedCert.hash}</p>
              </div>
              <div>
                <label className="block text-sm font-medium text-secondary-600 mb-1">Chain Hash</label>
                <p className="font-mono text-xs bg-secondary-50 p-2 rounded border break-all">{selectedCert.chain_hash}</p>
              </div>
            </div>
            <div className="flex items-center gap-2">
              <strong>Status:</strong>
              <Badge variant={selectedCert.status === 'active' ? 'success' : 'danger'}>
                {selectedCert.status}
              </Badge>
            </div>
            <div>
              <label className="block text-sm font-medium text-secondary-600 mb-1">Issued By</label>
              <p className="font-semibold">{selectedCert.issuer_id}</p>
            </div>
            
            {selectedCert.verifications && selectedCert.verifications.length > 0 && (
              <div>
                <p className="font-semibold mb-2">Verifier Details ({selectedCert.verifications.length})</p>
                <div className="space-y-2">
                  {selectedCert.verifications.map((v, idx) => (
                    <div key={idx} className="bg-secondary-50 p-3 rounded-lg border">
                      <div className="grid grid-cols-2 gap-2 text-sm">
                        <div>
                          <span className="text-secondary-600">Verifier:</span>
                          <span className="ml-2 font-medium">{v.verifier_id}</span>
                        </div>
                        <div>
                          <span className="text-secondary-600">Result:</span>
                          <Badge variant={v.result ? 'success' : 'danger'}>
                            {v.result ? '✓ Valid' : '✗ Invalid'}
                          </Badge>
                        </div>
                        <div>
                          <span className="text-secondary-600">Date:</span>
                          <span className="ml-2">{new Date(v.timestamp).toLocaleString()}</span>
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            )}
          </div>
        </InfoCard>
      )}
    </div>
  );

  return (
    <>
      <Layout
        title="Student Dashboard"
        subtitle="Manage your certificates and profile"
        userRole={profile?.name || 'Student'}
        onLogout={logout}
        navigationItems={navigationItems}
        activeTab={activeTab}
        onModuleChange={setActiveTab}
        themeColor="blue"
      >
        <div className="space-y-6">
              {activeTab === 'profile' && renderProfile()}
              {activeTab === 'certificates' && renderCertificates()}
            </div>
      </Layout>

    </>
  );
};

export default StudentDashboard;