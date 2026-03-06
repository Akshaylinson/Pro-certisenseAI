import React, { useState, useEffect } from 'react';
import axios from 'axios';

const API_URL = 'http://localhost:8000/api/student';

const StudentDashboardEnhanced = () => {
  const [activeModule, setActiveModule] = useState('dashboard');
  const [profile, setProfile] = useState(null);
  const [certificates, setCertificates] = useState([]);
  const [verifications, setVerifications] = useState([]);
  const [selectedCert, setSelectedCert] = useState(null);
  const [blockchainData, setBlockchainData] = useState(null);
  const [shareData, setShareData] = useState(null);
  const [feedbacks, setFeedbacks] = useState([]);
  const [dashboardStats, setDashboardStats] = useState(null);
  const [editMode, setEditMode] = useState(false);
  const [editData, setEditData] = useState({ name: '', email: '', phone: '' });
  const [loading, setLoading] = useState(false);

  const token = localStorage.getItem('token');
  const headers = { Authorization: `Bearer ${token}` };

  useEffect(() => {
    if (activeModule === 'dashboard') loadDashboard();
    else if (activeModule === 'profile') loadProfile();
    else if (activeModule === 'certificates') loadCertificates();
    else if (activeModule === 'verifications') loadVerifications();
    else if (activeModule === 'feedback') loadFeedbacks();
  }, [activeModule]);

  const loadDashboard = async () => {
    try {
      const res = await axios.get(`${API_URL}/dashboard`, { headers });
      setDashboardStats(res.data);
    } catch (err) {
      console.error(err);
    }
  };

  const loadProfile = async () => {
    try {
      const res = await axios.get(`${API_URL}/profile`, { headers });
      setProfile(res.data);
      setEditData({ name: res.data.name, email: res.data.email, phone: res.data.phone || '' });
    } catch (err) {
      console.error(err);
    }
  };

  const loadCertificates = async () => {
    setLoading(true);
    try {
      const res = await axios.get(`${API_URL}/certificates`, { headers });
      setCertificates(res.data.certificates);
    } catch (err) {
      console.error(err);
    }
    setLoading(false);
  };

  const loadVerifications = async () => {
    try {
      const res = await axios.get(`${API_URL}/verifications`, { headers });
      setVerifications(res.data.verifications);
    } catch (err) {
      console.error(err);
    }
  };

  const loadFeedbacks = async () => {
    try {
      const res = await axios.get(`${API_URL}/feedback`, { headers });
      setFeedbacks(res.data.feedbacks);
    } catch (err) {
      console.error(err);
    }
  };

  const handleProfileUpdate = async () => {
    try {
      await axios.put(
        `${API_URL}/profile?name=${editData.name}&email=${editData.email}&phone=${editData.phone}`,
        {},
        { headers }
      );
      setEditMode(false);
      loadProfile();
      alert('✅ Profile updated successfully');
    } catch (err) {
      alert('❌ Error updating profile');
    }
  };

  const viewCertificateDetails = async (certHash) => {
    try {
      const res = await axios.get(`${API_URL}/certificate/${certHash}`, { headers });
      setSelectedCert(res.data);
    } catch (err) {
      alert('❌ Error loading certificate details');
    }
  };

  const viewBlockchainDetails = async (certHash) => {
    try {
      const res = await axios.get(`${API_URL}/blockchain/${certHash}`, { headers });
      setBlockchainData(res.data);
      alert(`⛓️ Blockchain Details\n\nHash: ${res.data.certificate_hash.substring(0, 20)}...\nStatus: ${res.data.blockchain_validation_status}\nHash Match: ${res.data.hash_match ? '✅' : '❌'}`);
    } catch (err) {
      alert('❌ Error loading blockchain details');
    }
  };

  const generateShareLink = async (certHash) => {
    try {
      const res = await axios.post(`${API_URL}/certificate/${certHash}/share`, {}, { headers });
      setShareData(res.data);
      alert(`🔗 Share Link Generated!\n\nLink: ${res.data.verification_link}\n\nQR Code Data: ${res.data.qr_code_data}\n\nExpires in: ${res.data.expires_in}`);
    } catch (err) {
      alert('❌ Error generating share link');
    }
  };

  const flagVerification = async (verificationId) => {
    try {
      await axios.post(`${API_URL}/verifications/${verificationId}/flag`, {}, { headers });
      alert('🚩 Verification flagged as suspicious');
      loadVerifications();
    } catch (err) {
      alert('❌ Error flagging verification');
    }
  };

  const submitFeedback = async (e) => {
    e.preventDefault();
    const formData = new FormData(e.target);
    
    try {
      await axios.post(
        `${API_URL}/feedback?message=${encodeURIComponent(formData.get('message'))}&category=${formData.get('category')}`,
        {},
        { headers }
      );
      alert('✅ Feedback submitted successfully');
      e.target.reset();
      loadFeedbacks();
    } catch (err) {
      alert('❌ Feedback submission failed');
    }
  };

  const handleLogout = () => {
    localStorage.removeItem('token');
    window.location.href = '/';
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-50 to-blue-50">
      {/* Navigation */}
      <nav className="bg-gradient-to-r from-blue-600 to-blue-700 text-white shadow-xl">
        <div className="container mx-auto px-6 py-4 flex justify-between items-center">
          <div>
            <h1 className="text-3xl font-bold">🎓 Student Portal</h1>
            <p className="text-sm text-blue-100 mt-1">CertiSense AI v3.0</p>
          </div>
          <button onClick={handleLogout} className="bg-red-500 hover:bg-red-600 px-6 py-2 rounded-lg font-semibold transition shadow-lg">
            🚪 Logout
          </button>
        </div>
      </nav>

      <div className="container mx-auto mt-8 px-6">
        <div className="flex gap-6">
          {/* Sidebar */}
          <div className="w-72 bg-white rounded-xl shadow-xl p-6 h-fit sticky top-8">
            <h2 className="font-bold text-xl mb-6 text-gray-800 border-b pb-3">📋 Modules</h2>
            <ul className="space-y-2">
              {[
                { id: 'dashboard', label: '📊 Dashboard', desc: 'Overview' },
                { id: 'profile', label: '👤 My Profile', desc: 'View & Edit' },
                { id: 'certificates', label: '📜 Certificates', desc: 'View All' },
                { id: 'verifications', label: '🔍 Verifications', desc: 'Monitor Status' },
                { id: 'feedback', label: '💬 Feedback', desc: 'Submit Issues' }
              ].map(mod => (
                <li key={mod.id}>
                  <button
                    onClick={() => setActiveModule(mod.id)}
                    className={`w-full text-left px-4 py-3 rounded-lg transition shadow-sm ${
                      activeModule === mod.id 
                        ? 'bg-gradient-to-r from-blue-500 to-blue-600 text-white shadow-lg transform scale-105' 
                        : 'hover:bg-gray-50 text-gray-700 border border-gray-200'
                    }`}
                  >
                    <div className="font-semibold">{mod.label}</div>
                    <div className="text-xs opacity-80 mt-1">{mod.desc}</div>
                  </button>
                </li>
              ))}
            </ul>
          </div>

          {/* Main Content */}
          <div className="flex-1 bg-white rounded-xl shadow-xl p-8">
            {/* Dashboard Module */}
            {activeModule === 'dashboard' && dashboardStats && (
              <div>
                <h2 className="text-4xl font-bold mb-8 text-gray-800">📊 Dashboard</h2>
                
                <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-8">
                  <div className="bg-gradient-to-br from-blue-400 to-blue-600 text-white p-6 rounded-xl shadow-lg">
                    <h3 className="text-sm font-semibold mb-2 opacity-90">Total Certificates</h3>
                    <p className="text-5xl font-bold">{dashboardStats.statistics.total_certificates}</p>
                  </div>
                  <div className="bg-gradient-to-br from-green-400 to-green-600 text-white p-6 rounded-xl shadow-lg">
                    <h3 className="text-sm font-semibold mb-2 opacity-90">Active Certificates</h3>
                    <p className="text-5xl font-bold">{dashboardStats.statistics.active_certificates}</p>
                  </div>
                  <div className="bg-gradient-to-br from-purple-400 to-purple-600 text-white p-6 rounded-xl shadow-lg">
                    <h3 className="text-sm font-semibold mb-2 opacity-90">Total Verifications</h3>
                    <p className="text-5xl font-bold">{dashboardStats.statistics.total_verifications}</p>
                  </div>
                  <div className="bg-gradient-to-br from-orange-400 to-orange-600 text-white p-6 rounded-xl shadow-lg">
                    <h3 className="text-sm font-semibold mb-2 opacity-90">Recent (30d)</h3>
                    <p className="text-5xl font-bold">{dashboardStats.statistics.recent_verifications}</p>
                  </div>
                </div>

                <div className="bg-gradient-to-r from-indigo-50 to-purple-50 p-6 rounded-xl border border-indigo-200">
                  <h3 className="font-bold text-lg mb-4">👤 Student Information</h3>
                  <div className="space-y-2">
                    <p><strong>Name:</strong> {dashboardStats.student_info.name}</p>
                    <p><strong>Student ID:</strong> {dashboardStats.student_info.student_id}</p>
                    <p><strong>Email:</strong> {dashboardStats.student_info.email}</p>
                  </div>
                </div>
              </div>
            )}

            {/* Profile Module */}
            {activeModule === 'profile' && profile && (
              <div>
                <h2 className="text-4xl font-bold mb-8 text-gray-800">👤 My Profile</h2>
                
                {!editMode ? (
                  <div className="bg-gradient-to-r from-gray-50 to-gray-100 p-8 rounded-xl border-2 border-gray-200 space-y-4">
                    <div className="grid grid-cols-2 gap-4">
                      <div>
                        <p className="text-sm text-gray-600">Student ID</p>
                        <p className="text-lg font-semibold">{profile.student_id}</p>
                      </div>
                      <div>
                        <p className="text-sm text-gray-600">Account Status</p>
                        <p className="text-lg font-semibold text-green-600">{profile.account_status}</p>
                      </div>
                      <div>
                        <p className="text-sm text-gray-600">Name</p>
                        <p className="text-lg font-semibold">{profile.name}</p>
                      </div>
                      <div>
                        <p className="text-sm text-gray-600">Email</p>
                        <p className="text-lg font-semibold">{profile.email}</p>
                      </div>
                      <div>
                        <p className="text-sm text-gray-600">Phone</p>
                        <p className="text-lg font-semibold">{profile.phone || 'N/A'}</p>
                      </div>
                      <div>
                        <p className="text-sm text-gray-600">Program</p>
                        <p className="text-lg font-semibold">{profile.program || 'N/A'}</p>
                      </div>
                      <div>
                        <p className="text-sm text-gray-600">Department</p>
                        <p className="text-lg font-semibold">{profile.department || 'N/A'}</p>
                      </div>
                      <div>
                        <p className="text-sm text-gray-600">Institute</p>
                        <p className="text-lg font-semibold">{profile.institute_name}</p>
                      </div>
                    </div>
                    <button onClick={() => setEditMode(true)} className="mt-6 bg-blue-600 text-white px-6 py-3 rounded-lg hover:bg-blue-700 font-semibold shadow-md">
                      ✏️ Edit Profile
                    </button>
                  </div>
                ) : (
                  <div className="space-y-4 bg-blue-50 p-8 rounded-xl border-2 border-blue-200">
                    <div>
                      <label className="block font-semibold mb-2">Name</label>
                      <input
                        type="text"
                        value={editData.name}
                        onChange={(e) => setEditData({ ...editData, name: e.target.value })}
                        className="w-full px-4 py-3 border-2 border-gray-300 rounded-lg focus:border-blue-500 focus:outline-none"
                      />
                    </div>
                    <div>
                      <label className="block font-semibold mb-2">Email</label>
                      <input
                        type="email"
                        value={editData.email}
                        onChange={(e) => setEditData({ ...editData, email: e.target.value })}
                        className="w-full px-4 py-3 border-2 border-gray-300 rounded-lg focus:border-blue-500 focus:outline-none"
                      />
                    </div>
                    <div>
                      <label className="block font-semibold mb-2">Phone</label>
                      <input
                        type="text"
                        value={editData.phone}
                        onChange={(e) => setEditData({ ...editData, phone: e.target.value })}
                        className="w-full px-4 py-3 border-2 border-gray-300 rounded-lg focus:border-blue-500 focus:outline-none"
                      />
                    </div>
                    <div className="flex gap-3 mt-6">
                      <button onClick={handleProfileUpdate} className="flex-1 bg-green-600 text-white px-6 py-3 rounded-lg hover:bg-green-700 font-semibold shadow-md">
                        💾 Save Changes
                      </button>
                      <button onClick={() => setEditMode(false)} className="flex-1 bg-gray-600 text-white px-6 py-3 rounded-lg hover:bg-gray-700 font-semibold shadow-md">
                        ❌ Cancel
                      </button>
                    </div>
                  </div>
                )}
              </div>
            )}

            {/* Certificates Module */}
            {activeModule === 'certificates' && (
              <div>
                <h2 className="text-4xl font-bold mb-8 text-gray-800">📜 My Certificates</h2>
                
                {loading ? (
                  <div className="text-center py-12">Loading certificates...</div>
                ) : certificates.length === 0 ? (
                  <div className="text-center py-12 text-gray-600">No certificates issued yet</div>
                ) : (
                  <div className="space-y-4">
                    {certificates.map((cert, idx) => (
                      <div key={idx} className="border-2 border-gray-200 p-6 rounded-xl hover:shadow-lg transition bg-gradient-to-r from-white to-gray-50">
                        <div className="flex justify-between items-start">
                          <div className="flex-1">
                            <h3 className="font-bold text-lg text-gray-800">{cert.certificate_name}</h3>
                            <p className="text-sm text-gray-600 mt-2">Hash: {cert.certificate_hash.substring(0, 20)}...</p>
                            <p className="text-sm text-gray-600">Type: {cert.certificate_type || 'General'}</p>
                            <p className="text-sm text-gray-600">Issued: {cert.issue_date ? new Date(cert.issue_date).toLocaleDateString() : 'N/A'}</p>
                            <p className="text-sm text-gray-600">Verifications: {cert.verification_count}</p>
                          </div>
                          <span className={`px-4 py-2 rounded-lg font-bold ${
                            cert.status === 'active' ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'
                          }`}>
                            {cert.status.toUpperCase()}
                          </span>
                        </div>
                        <div className="mt-4 flex gap-2 flex-wrap">
                          <button
                            onClick={() => viewCertificateDetails(cert.certificate_hash)}
                            className="bg-blue-500 text-white px-4 py-2 rounded-lg hover:bg-blue-600 text-sm font-semibold"
                          >
                            📄 View Details
                          </button>
                          <button
                            onClick={() => viewBlockchainDetails(cert.certificate_hash)}
                            className="bg-purple-500 text-white px-4 py-2 rounded-lg hover:bg-purple-600 text-sm font-semibold"
                          >
                            ⛓️ Blockchain
                          </button>
                          <button
                            onClick={() => generateShareLink(cert.certificate_hash)}
                            className="bg-green-500 text-white px-4 py-2 rounded-lg hover:bg-green-600 text-sm font-semibold"
                          >
                            🔗 Share
                          </button>
                        </div>
                      </div>
                    ))}
                  </div>
                )}

                {selectedCert && (
                  <div className="mt-8 bg-blue-50 p-6 rounded-xl border-2 border-blue-200">
                    <h3 className="font-bold text-xl mb-4">📋 Certificate Details</h3>
                    <div className="grid grid-cols-2 gap-4 text-sm">
                      <div><strong>Certificate ID:</strong> {selectedCert.certificate_id}</div>
                      <div><strong>Status:</strong> {selectedCert.status}</div>
                      <div><strong>Type:</strong> {selectedCert.certificate_type || 'N/A'}</div>
                      <div><strong>Issuing Institute:</strong> {selectedCert.issuing_institute}</div>
                      <div className="col-span-2"><strong>Hash:</strong> {selectedCert.certificate_hash}</div>
                      <div className="col-span-2"><strong>Chain Hash:</strong> {selectedCert.chain_hash}</div>
                    </div>
                  </div>
                )}
              </div>
            )}

            {/* Verifications Module */}
            {activeModule === 'verifications' && (
              <div>
                <h2 className="text-4xl font-bold mb-8 text-gray-800">🔍 Verification History</h2>
                
                {verifications.length === 0 ? (
                  <div className="text-center py-12 text-gray-600">No verifications yet</div>
                ) : (
                  <div className="overflow-x-auto rounded-xl border-2 border-gray-200">
                    <table className="w-full">
                      <thead className="bg-gradient-to-r from-gray-100 to-gray-200">
                        <tr>
                          <th className="p-4 text-left font-bold">Certificate</th>
                          <th className="p-4 text-left font-bold">Verifier ID</th>
                          <th className="p-4 text-center font-bold">Status</th>
                          <th className="p-4 text-center font-bold">Confidence</th>
                          <th className="p-4 text-left font-bold">Date</th>
                          <th className="p-4 text-center font-bold">Action</th>
                        </tr>
                      </thead>
                      <tbody>
                        {verifications.map((v, idx) => (
                          <tr key={idx} className={`border-b hover:bg-gray-50 ${idx % 2 === 0 ? 'bg-white' : 'bg-gray-50'}`}>
                            <td className="p-4 text-sm">{v.certificate_name}</td>
                            <td className="p-4 text-sm font-mono">{v.verifier_id.substring(0, 12)}...</td>
                            <td className="p-4 text-center">
                              <span className={`px-3 py-1 rounded-lg text-xs font-bold ${
                                v.result ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'
                              }`}>
                                {v.verification_status}
                              </span>
                            </td>
                            <td className="p-4 text-center font-semibold">{v.confidence_score ? (v.confidence_score * 100).toFixed(1) + '%' : 'N/A'}</td>
                            <td className="p-4 text-sm">{new Date(v.timestamp).toLocaleString()}</td>
                            <td className="p-4 text-center">
                              {!v.is_suspicious && (
                                <button
                                  onClick={() => flagVerification(v.verification_id)}
                                  className="bg-red-500 text-white px-3 py-1 rounded text-xs hover:bg-red-600"
                                >
                                  🚩 Flag
                                </button>
                              )}
                              {v.is_suspicious && <span className="text-red-600 font-bold">Flagged</span>}
                            </td>
                          </tr>
                        ))}
                      </tbody>
                    </table>
                  </div>
                )}
              </div>
            )}

            {/* Feedback Module */}
            {activeModule === 'feedback' && (
              <div>
                <h2 className="text-4xl font-bold mb-8 text-gray-800">💬 Submit Feedback</h2>
                
                <form onSubmit={submitFeedback} className="space-y-6 mb-10 bg-gradient-to-r from-blue-50 to-indigo-50 p-8 rounded-xl border-2 border-blue-200">
                  <div>
                    <label className="block font-bold mb-2">Category</label>
                    <select name="category" className="w-full px-4 py-3 border-2 border-gray-300 rounded-lg focus:border-blue-500 focus:outline-none" required>
                      <option value="suspicious_verification">🚨 Suspicious Verification</option>
                      <option value="incorrect_info">⚠️ Incorrect Information</option>
                      <option value="general">💡 General Feedback</option>
                    </select>
                  </div>

                  <div>
                    <label className="block font-bold mb-2">Message</label>
                    <textarea
                      name="message"
                      rows="5"
                      className="w-full px-4 py-3 border-2 border-gray-300 rounded-lg focus:border-blue-500 focus:outline-none"
                      placeholder="Describe your feedback..."
                      required
                    ></textarea>
                  </div>

                  <button type="submit" className="w-full bg-gradient-to-r from-blue-600 to-indigo-600 text-white px-6 py-4 rounded-lg hover:from-blue-700 hover:to-indigo-700 font-bold text-lg shadow-lg">
                    📤 Submit Feedback
                  </button>
                </form>

                <h3 className="font-bold text-2xl mb-6">📋 My Feedback</h3>
                <div className="space-y-4">
                  {feedbacks.map(fb => (
                    <div key={fb.id} className="bg-gradient-to-r from-gray-50 to-gray-100 p-6 rounded-xl border-2 border-gray-200">
                      <div className="flex justify-between items-start">
                        <div>
                          <p className="font-bold text-lg">{fb.category}</p>
                          <p className="text-gray-600 mt-2">{fb.message}</p>
                        </div>
                        <span className={`px-3 py-1 rounded-lg text-xs font-bold ${
                          fb.status === 'open' ? 'bg-yellow-100 text-yellow-800' : 'bg-green-100 text-green-800'
                        }`}>
                          {fb.status}
                        </span>
                      </div>
                      <p className="text-xs text-gray-500 mt-3">{new Date(fb.timestamp).toLocaleString()}</p>
                    </div>
                  ))}
                </div>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default StudentDashboardEnhanced;
