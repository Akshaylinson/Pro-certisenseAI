import React, { useState, useEffect } from 'react';
import { useAuth } from '../contexts/AuthContext';

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
    <div className="space-y-4">
      <h3 className="text-lg font-semibold">My Profile</h3>
      
      {!editMode ? (
        <div className="bg-gray-50 p-4 rounded-lg space-y-2">
          <p><span className="font-medium">Student ID:</span> {profile?.student_id}</p>
          <p><span className="font-medium">Name:</span> {profile?.name}</p>
          <p><span className="font-medium">Email:</span> {profile?.email}</p>
          <p><span className="font-medium">Joined:</span> {new Date(profile?.created_at).toLocaleDateString()}</p>
          <button onClick={() => setEditMode(true)} className="mt-4 px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700">
            Edit Profile
          </button>
        </div>
      ) : (
        <div className="space-y-3">
          <input
            type="text"
            value={editData.name}
            onChange={(e) => setEditData({ ...editData, name: e.target.value })}
            className="w-full px-3 py-2 border rounded-md"
            placeholder="Name"
          />
          <input
            type="email"
            value={editData.email}
            onChange={(e) => setEditData({ ...editData, email: e.target.value })}
            className="w-full px-3 py-2 border rounded-md"
            placeholder="Email"
          />
          <div className="flex gap-2">
            <button onClick={handleProfileUpdate} className="px-4 py-2 bg-green-600 text-white rounded hover:bg-green-700">
              Save
            </button>
            <button onClick={() => setEditMode(false)} className="px-4 py-2 bg-gray-600 text-white rounded hover:bg-gray-700">
              Cancel
            </button>
          </div>
        </div>
      )}
    </div>
  );

  const renderCertificates = () => (
    <div className="space-y-4">
      <h3 className="text-lg font-semibold">My Certificates</h3>
      
      {loading ? (
        <div className="text-center py-8">Loading certificates...</div>
      ) : certificates.length === 0 ? (
        <div className="text-center py-8 text-gray-600">No certificates issued yet</div>
      ) : (
        <div className="space-y-3">
          {certificates.map((cert, idx) => (
            <div key={idx} className="border p-4 rounded-lg hover:shadow-md">
              <div className="flex justify-between items-center">
                <div className="flex-1">
                  <p className="font-medium">{cert.name || `Certificate ${idx + 1}`}</p>
                  <p className="text-sm text-gray-600">ID: {cert.certificate_id}</p>
                  <p className="text-sm text-gray-600">Hash: {cert.hash?.substring(0, 16)}...</p>
                  <p className="text-sm text-gray-600">Issued: {cert.issue_date ? new Date(cert.issue_date).toLocaleDateString() : 'N/A'}</p>
                  <p className="text-sm text-gray-600">Verifications: {cert.verification_count || 0}</p>
                </div>
                <div className="flex flex-col gap-2">
                  <span className={`px-3 py-1 rounded text-white text-center ${cert.status === 'active' ? 'bg-green-500' : 'bg-red-500'}`}>
                    {cert.status === 'active' ? 'Valid' : 'Revoked'}
                  </span>
                  <a
                    href={`http://localhost:8000/student/certificates/${cert.certificate_id}/download`}
                    target="_blank"
                    rel="noopener noreferrer"
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
                    className="px-3 py-1 bg-blue-600 text-white rounded hover:bg-blue-700 text-center text-sm"
                  >
                    Download
                  </a>
                  <button
                    onClick={() => cert.hash && loadCertificateDetails(cert.hash)}
                    className="px-3 py-1 bg-gray-600 text-white rounded hover:bg-gray-700 text-sm"
                  >
                    Details
                  </button>
                </div>
              </div>
            </div>
          ))}
        </div>
      )}

      {selectedCert && (
        <div className="mt-6 bg-blue-50 p-4 rounded-lg">
          <h4 className="font-semibold mb-3">Certificate Details</h4>
          <div className="space-y-2 text-sm">
            <p><span className="font-medium">Hash:</span> {selectedCert.hash}</p>
            <p><span className="font-medium">Chain Hash:</span> {selectedCert.chain_hash}</p>
            <p><span className="font-medium">Status:</span> {selectedCert.status}</p>
            <p><span className="font-medium">Issued By:</span> {selectedCert.issuer_id}</p>
            <p><span className="font-medium">Verifications:</span> {selectedCert.verifications?.length || 0}</p>
            
            {selectedCert.verifications && selectedCert.verifications.length > 0 && (
              <div className="mt-3">
                <p className="font-medium">Verifier Details:</p>
                <div className="mt-2 space-y-1">
                  {selectedCert.verifications.map((v, idx) => (
                    <div key={idx} className="text-xs bg-white p-2 rounded">
                      <p>Verifier: {v.verifier_id}</p>
                      <p>Result: {v.result ? '✓ Valid' : '✗ Invalid'}</p>
                      <p>Date: {new Date(v.timestamp).toLocaleString()}</p>
                    </div>
                  ))}
                </div>
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  );

  return (
    <div className="min-h-screen bg-gray-50">
      <nav className="bg-white shadow-sm border-b">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between h-16">
            <div className="flex items-center">
              <h1 className="text-xl font-semibold">Student Dashboard</h1>
            </div>
            <div className="flex items-center space-x-4">
              <span className="text-sm text-gray-600">Welcome, {profile?.name}</span>
              <button onClick={logout} className="px-3 py-1 bg-red-500 text-white rounded hover:bg-red-600">
                Logout
              </button>
            </div>
          </div>
        </div>
      </nav>

      <div className="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
        <div className="flex space-x-8">
          <div className="w-64">
            <nav className="space-y-1">
              {[
                { key: 'profile', label: 'My Profile' },
                { key: 'certificates', label: 'My Certificates' }
              ].map(tab => (
                <button
                  key={tab.key}
                  onClick={() => setActiveTab(tab.key)}
                  className={`w-full text-left px-3 py-2 rounded-md text-sm font-medium ${
                    activeTab === tab.key
                      ? 'bg-blue-100 text-blue-700'
                      : 'text-gray-600 hover:bg-gray-50'
                  }`}
                >
                  {tab.label}
                </button>
              ))}
            </nav>
          </div>

          <div className="flex-1">
            <div className="bg-white shadow rounded-lg p-6">
              {activeTab === 'profile' && renderProfile()}
              {activeTab === 'certificates' && renderCertificates()}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default StudentDashboard;