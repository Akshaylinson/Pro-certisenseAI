import React, { useState, useEffect } from 'react';
import axios from 'axios';
import ReportDialog from './ReportDialog';

const API_URL = 'http://localhost:8000';

const AdminDashboard = () => {
  const [activeModule, setActiveModule] = useState('dashboard');
  const [analytics, setAnalytics] = useState(null);
  const [institutes, setInstitutes] = useState([]);
  const [certificates, setCertificates] = useState([]);
  const [students, setStudents] = useState([]);
  const [verifiers, setVerifiers] = useState([]);
  const [verifications, setVerifications] = useState([]);
  const [feedbacks, setFeedbacks] = useState([]);
  const [loading, setLoading] = useState(false);
  const [showInstituteForm, setShowInstituteForm] = useState(false);
  const [showVerifierForm, setShowVerifierForm] = useState(false);
  const [formData, setFormData] = useState({});
  
  // Report dialog state
  const [showReportDialog, setShowReportDialog] = useState(false);
  const [reportData, setReportData] = useState(null);
  const [reportType, setReportType] = useState('');
  const [reportLoading, setReportLoading] = useState(false);

  const token = localStorage.getItem('admin_token');
  const headers = { Authorization: `Bearer ${token}` };

  useEffect(() => {
    loadModuleData();
  }, [activeModule]);

  const loadModuleData = () => {
    if (activeModule === 'dashboard') loadAnalytics();
    else if (activeModule === 'institutes') loadInstitutes();
    else if (activeModule === 'certificates') loadCertificates();
    else if (activeModule === 'students') loadStudents();
    else if (activeModule === 'verifiers') loadVerifiers();
    else if (activeModule === 'verifications') loadVerifications();
    else if (activeModule === 'feedback') loadFeedbacks();
  };

  const loadAnalytics = async () => {
    setLoading(true);
    try {
      const res = await axios.get(`${API_URL}/admin/analytics`, { headers });
      setAnalytics(res.data);
    } catch (err) {
      console.error('Analytics error:', err);
    }
    setLoading(false);
  };

  const loadInstitutes = async () => {
    setLoading(true);
    try {
      const res = await axios.get(`${API_URL}/admin/institutes`, { headers });
      setInstitutes(res.data.institutes);
    } catch (err) {
      console.error('Institutes error:', err);
    }
    setLoading(false);
  };

  const loadCertificates = async () => {
    setLoading(true);
    try {
      console.log('Loading certificates...');
      const res = await axios.get(`${API_URL}/admin/certificates`, { headers });
      console.log('Certificates API response:', res.data);
      console.log('Certificates array:', res.data.certificates);
      setCertificates(res.data.certificates);
      console.log('Certificates state set to:', res.data.certificates);
    } catch (err) {
      console.error('Certificates error:', err);
      console.error('Error response:', err.response?.data);
    }
    setLoading(false);
  };

  const loadStudents = async () => {
    setLoading(true);
    try {
      console.log('Loading students...');
      const res = await axios.get(`${API_URL}/admin/students`, { headers });
      console.log('Students API response:', res.data);
      console.log('Students array:', res.data.students);
      setStudents(res.data.students);
      console.log('Students state set to:', res.data.students);
    } catch (err) {
      console.error('Students error:', err);
      console.error('Error response:', err.response?.data);
    }
    setLoading(false);
  };

  const loadVerifiers = async () => {
    setLoading(true);
    try {
      const res = await axios.get(`${API_URL}/admin/verifiers`, { headers });
      setVerifiers(res.data.verifiers);
    } catch (err) {
      console.error('Verifiers error:', err);
    }
    setLoading(false);
  };

  const loadVerifications = async () => {
    setLoading(true);
    try {
      const res = await axios.get(`${API_URL}/admin/verifications`, { headers });
      setVerifications(res.data.verifications);
    } catch (err) {
      console.error('Verifications error:', err);
    }
    setLoading(false);
  };

  const loadFeedbacks = async () => {
    setLoading(true);
    try {
      const res = await axios.get(`${API_URL}/admin/feedback`, { headers });
      setFeedbacks(res.data.feedbacks);
    } catch (err) {
      console.error('Feedback error:', err);
    }
    setLoading(false);
  };

  const deleteInstitute = async (id) => {
    if (!window.confirm('Delete this institute?')) return;
    try {
      await axios.delete(`${API_URL}/admin/institutes/${id}`, { headers });
      alert('Institute deleted successfully');
      loadInstitutes();
    } catch (err) {
      alert(err.response?.data?.detail || 'Delete failed');
    }
  };

  const deleteVerifier = async (id) => {
    if (!window.confirm('Delete this verifier?')) return;
    try {
      await axios.delete(`${API_URL}/admin/verifiers/${id}`, { headers });
      alert('Verifier deleted successfully');
      loadVerifiers();
    } catch (err) {
      alert(err.response?.data?.detail || 'Delete failed');
    }
  };

  const flagVerification = async (id) => {
    try {
      await axios.put(`${API_URL}/admin/verifications/${id}/flag`, {}, { headers });
      alert('Verification flagged as suspicious');
      loadVerifications();
    } catch (err) {
      alert('Flag operation failed');
    }
  };

  const flagFeedback = async (id) => {
    try {
      await axios.put(`${API_URL}/admin/feedback/${id}/flag`, {}, { headers });
      alert('Feedback flagged for follow-up');
      loadFeedbacks();
    } catch (err) {
      alert('Flag operation failed');
    }
  };

  const addInstitute = async (e) => {
    e.preventDefault();
    try {
      await axios.post(`${API_URL}/admin/institutes`, null, {
        params: {
          institute_name: formData.name,
          email: formData.email,
          password: formData.password,
          location: formData.location
        },
        headers
      });
      alert('Institute added successfully');
      setShowInstituteForm(false);
      setFormData({});
      loadInstitutes();
    } catch (err) {
      alert(err.response?.data?.detail || 'Failed to add institute');
    }
  };

  const addVerifier = async (e) => {
    e.preventDefault();
    try {
      await axios.post(`${API_URL}/auth/verifier/register`, {
        username: formData.username,
        email: formData.email,
        password: formData.password
      });
      alert('Verifier added successfully');
      setShowVerifierForm(false);
      setFormData({});
      loadVerifiers();
    } catch (err) {
      alert(err.response?.data?.detail || 'Failed to add verifier');
    }
  };

  const handleLogout = () => {
    localStorage.removeItem('admin_token');
    window.location.href = '/';
  };

  const generateReport = async (type) => {
    setReportType(type);
    setReportLoading(true);
    setShowReportDialog(true);
    
    try {
      const response = await axios.get(`${API_URL}/admin/reports/${type}`, { headers });
      setReportData(response.data);
    } catch (error) {
      console.error('Report generation error:', error);
      alert('Failed to generate report. Please try again.');
      setShowReportDialog(false);
    } finally {
      setReportLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-100">
      {/* Top Navigation */}
      <nav className="bg-blue-600 text-white shadow-lg">
        <div className="container mx-auto px-4 py-4 flex justify-between items-center">
          <div>
            <h1 className="text-2xl font-bold">🔐 CertiSense AI v3.0</h1>
            <p className="text-sm text-blue-200">Admin Control System</p>
          </div>
          <button 
            onClick={handleLogout} 
            className="bg-red-500 hover:bg-red-600 px-6 py-2 rounded-lg font-semibold transition"
          >
            Logout
          </button>
        </div>
      </nav>

      <div className="container mx-auto mt-6 px-4">
        <div className="flex gap-6">
          {/* Sidebar Navigation */}
          <div className="w-64 bg-white rounded-lg shadow-lg p-4 h-fit">
            <h2 className="font-bold text-lg mb-4 text-gray-700">Admin Modules</h2>
            <ul className="space-y-2">
              {[
                { id: 'dashboard', label: '📊 Dashboard', icon: '📊' },
                { id: 'institutes', label: '🏫 Institutes', icon: '🏫' },
                { id: 'certificates', label: '📜 Certificates', icon: '📜' },
                { id: 'students', label: '👨‍🎓 Students', icon: '👨‍🎓' },
                { id: 'verifiers', label: '🔍 Verifiers', icon: '🔍' },
                { id: 'verifications', label: '✅ Verifications', icon: '✅' },
                { id: 'reports', label: '📈 Reports', icon: '📈' },
                { id: 'feedback', label: '💬 Feedback', icon: '💬' }
              ].map(mod => (
                <li key={mod.id}>
                  <button
                    onClick={() => setActiveModule(mod.id)}
                    className={`w-full text-left px-4 py-3 rounded-lg transition ${
                      activeModule === mod.id 
                        ? 'bg-blue-500 text-white shadow-md' 
                        : 'hover:bg-gray-100 text-gray-700'
                    }`}
                  >
                    {mod.label}
                  </button>
                </li>
              ))}
            </ul>
          </div>

          {/* Main Content Area */}
          <div className="flex-1 bg-white rounded-lg shadow-lg p-6">
            {loading && (
              <div className="text-center py-12">
                <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-500 mx-auto"></div>
                <p className="mt-4 text-gray-600">Loading...</p>
              </div>
            )}

            {/* MODULE 1: Dashboard Analytics */}
            {activeModule === 'dashboard' && analytics && !loading && (
              <div>
                <h2 className="text-3xl font-bold mb-6 text-gray-800">System Analytics</h2>
                
                {/* Key Metrics */}
                <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-8">
                  <div className="bg-gradient-to-br from-blue-400 to-blue-600 text-white p-6 rounded-lg shadow">
                    <h3 className="text-sm font-semibold mb-2">Total Institutes</h3>
                    <p className="text-4xl font-bold">{analytics.total_institutes}</p>
                  </div>
                  <div className="bg-gradient-to-br from-green-400 to-green-600 text-white p-6 rounded-lg shadow">
                    <h3 className="text-sm font-semibold mb-2">Total Students</h3>
                    <p className="text-4xl font-bold">{analytics.total_students}</p>
                  </div>
                  <div className="bg-gradient-to-br from-yellow-400 to-yellow-600 text-white p-6 rounded-lg shadow">
                    <h3 className="text-sm font-semibold mb-2">Total Certificates</h3>
                    <p className="text-4xl font-bold">{analytics.total_certificates}</p>
                  </div>
                  <div className="bg-gradient-to-br from-purple-400 to-purple-600 text-white p-6 rounded-lg shadow">
                    <h3 className="text-sm font-semibold mb-2">Total Verifications</h3>
                    <p className="text-4xl font-bold">{analytics.total_verifications}</p>
                  </div>
                </div>

                {/* Performance Metrics */}
                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                  <div className="bg-gray-50 p-6 rounded-lg border">
                    <h3 className="font-bold text-lg mb-4">Verification Success Rate</h3>
                    <div className="flex items-center">
                      <div className="text-5xl font-bold text-green-600">{analytics.verification_success_rate}%</div>
                      <div className="ml-4 text-sm text-gray-600">
                        <p>✅ Successful verifications</p>
                        <p>📊 System performance indicator</p>
                      </div>
                    </div>
                  </div>

                  <div className="bg-gray-50 p-6 rounded-lg border">
                    <h3 className="font-bold text-lg mb-4">Certificate Status Distribution</h3>
                    <div className="space-y-2">
                      <div className="flex justify-between items-center">
                        <span className="text-green-600">● Active</span>
                        <span className="font-bold">{analytics.certificate_status.active}</span>
                      </div>
                      <div className="flex justify-between items-center">
                        <span className="text-red-600">● Revoked</span>
                        <span className="font-bold">{analytics.certificate_status.revoked}</span>
                      </div>
                      <div className="flex justify-between items-center">
                        <span className="text-orange-600">● Suspicious</span>
                        <span className="font-bold">{analytics.certificate_status.suspicious}</span>
                      </div>
                    </div>
                  </div>
                </div>

                {/* Recent Activity */}
                <div className="mt-6 bg-blue-50 p-6 rounded-lg border border-blue-200">
                  <h3 className="font-bold text-lg mb-2">Recent Activity (30 Days)</h3>
                  <div className="grid grid-cols-2 gap-4">
                    <div>
                      <p className="text-gray-600">New Certificates</p>
                      <p className="text-2xl font-bold text-blue-600">{analytics.recent_certificates_30d}</p>
                    </div>
                    <div>
                      <p className="text-gray-600">New Verifications</p>
                      <p className="text-2xl font-bold text-blue-600">{analytics.recent_verifications_30d}</p>
                    </div>
                  </div>
                </div>
              </div>
            )}

            {/* MODULE 2: Manage Institutes */}
            {activeModule === 'institutes' && !loading && (
              <div>
                <div className="flex justify-between items-center mb-6">
                  <h2 className="text-3xl font-bold text-gray-800">Manage Institutes</h2>
                  <button
                    onClick={() => setShowInstituteForm(true)}
                    className="bg-blue-500 text-white px-6 py-2 rounded-lg hover:bg-blue-600 font-semibold"
                  >
                    + Add Institute
                  </button>
                </div>

                {showInstituteForm && (
                  <div className="mb-6 bg-gray-50 p-6 rounded-lg border">
                    <h3 className="font-bold text-lg mb-4">Add New Institute</h3>
                    <form onSubmit={addInstitute} className="space-y-4">
                      <div>
                        <label className="block font-semibold mb-2">Institute Name *</label>
                        <input
                          type="text"
                          required
                          className="w-full px-4 py-2 border rounded-lg"
                          value={formData.name || ''}
                          onChange={(e) => setFormData({...formData, name: e.target.value})}
                        />
                      </div>
                      <div>
                        <label className="block font-semibold mb-2">Email *</label>
                        <input
                          type="email"
                          required
                          className="w-full px-4 py-2 border rounded-lg"
                          value={formData.email || ''}
                          onChange={(e) => setFormData({...formData, email: e.target.value})}
                        />
                      </div>
                      <div>
                        <label className="block font-semibold mb-2">Password *</label>
                        <input
                          type="password"
                          required
                          minLength="6"
                          className="w-full px-4 py-2 border rounded-lg"
                          value={formData.password || ''}
                          onChange={(e) => setFormData({...formData, password: e.target.value})}
                        />
                      </div>
                      <div>
                        <label className="block font-semibold mb-2">Location</label>
                        <input
                          type="text"
                          className="w-full px-4 py-2 border rounded-lg"
                          value={formData.location || ''}
                          onChange={(e) => setFormData({...formData, location: e.target.value})}
                        />
                      </div>
                      <div className="flex gap-2">
                        <button type="submit" className="bg-green-500 text-white px-6 py-2 rounded-lg hover:bg-green-600">
                          Create Institute
                        </button>
                        <button
                          type="button"
                          onClick={() => {setShowInstituteForm(false); setFormData({});}}
                          className="bg-gray-500 text-white px-6 py-2 rounded-lg hover:bg-gray-600"
                        >
                          Cancel
                        </button>
                      </div>
                    </form>
                  </div>
                )}
                <div className="overflow-x-auto">
                  <table className="w-full border-collapse">
                    <thead>
                      <tr className="bg-gray-200">
                        <th className="p-3 text-left">Institute ID</th>
                        <th className="p-3 text-left">Name</th>
                        <th className="p-3 text-left">Email</th>
                        <th className="p-3 text-left">Location</th>
                        <th className="p-3 text-center">Students</th>
                        <th className="p-3 text-center">Certificates</th>
                        <th className="p-3 text-center">Status</th>
                        <th className="p-3 text-center">Actions</th>
                      </tr>
                    </thead>
                    <tbody>
                      {institutes.map(inst => (
                        <tr key={inst.id} className="border-b hover:bg-gray-50">
                          <td className="p-3 font-mono text-sm">{inst.institute_id}</td>
                          <td className="p-3 font-semibold">{inst.name}</td>
                          <td className="p-3 text-sm">{inst.email}</td>
                          <td className="p-3 text-sm">{inst.location || 'N/A'}</td>
                          <td className="p-3 text-center">{inst.student_count}</td>
                          <td className="p-3 text-center">{inst.certificate_count}</td>
                          <td className="p-3 text-center">
                            <span className={`px-2 py-1 rounded text-xs ${
                              inst.approval_status === 'approved' ? 'bg-green-100 text-green-800' : 'bg-yellow-100 text-yellow-800'
                            }`}>
                              {inst.approval_status}
                            </span>
                          </td>
                          <td className="p-3 text-center">
                            <button 
                              onClick={() => deleteInstitute(inst.id)} 
                              className="text-red-500 hover:text-red-700 font-semibold"
                            >
                              Delete
                            </button>
                          </td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              </div>
            )}

            {/* MODULE 3: Manage Certificates */}
            {activeModule === 'certificates' && !loading && (
              <div>
                <h2 className="text-3xl font-bold mb-6 text-gray-800">Manage Certificates</h2>
                {certificates.length === 0 ? (
                  <div className="text-center py-12 bg-gray-50 rounded-lg">
                    <p className="text-gray-600 text-lg">No certificates found in the system.</p>
                    <p className="text-gray-500 text-sm mt-2">Certificates will appear here once institutes issue them to students.</p>
                  </div>
                ) : (
                  <div className="overflow-x-auto">
                    <table className="w-full border-collapse text-sm">
                      <thead>
                        <tr className="bg-gray-200">
                          <th className="p-3 text-left">Certificate ID</th>
                          <th className="p-3 text-left">Student</th>
                          <th className="p-3 text-left">Institute</th>
                          <th className="p-3 text-center">Status</th>
                          <th className="p-3 text-center">Verifications</th>
                          <th className="p-3 text-left">Issue Date</th>
                        </tr>
                      </thead>
                      <tbody>
                        {certificates.map(cert => (
                          <tr key={cert.id} className="border-b hover:bg-gray-50">
                            <td className="p-3 font-mono text-xs">{cert.id.slice(0, 12)}...</td>
                            <td className="p-3">{cert.student_name}</td>
                            <td className="p-3">{cert.institute_name}</td>
                            <td className="p-3 text-center">
                              <span className={`px-2 py-1 rounded text-xs ${
                                cert.status === 'active' ? 'bg-green-100 text-green-800' :
                                cert.status === 'revoked' ? 'bg-red-100 text-red-800' :
                                'bg-orange-100 text-orange-800'
                              }`}>
                                {cert.status}
                              </span>
                            </td>
                            <td className="p-3 text-center font-semibold">{cert.verification_count}</td>
                            <td className="p-3 text-xs">{cert.issue_date ? new Date(cert.issue_date).toLocaleDateString() : 'N/A'}</td>
                          </tr>
                        ))}
                      </tbody>
                    </table>
                  </div>
                )}
              </div>
            )}

            {/* MODULE 4: View Students */}
            {activeModule === 'students' && !loading && (
              <div>
                <h2 className="text-3xl font-bold mb-6 text-gray-800">View Students (Read-Only)</h2>
                {students.length === 0 ? (
                  <div className="text-center py-12 bg-gray-50 rounded-lg">
                    <p className="text-gray-600 text-lg">No students found in the system.</p>
                    <p className="text-gray-500 text-sm mt-2">Students will appear here once institutes add them.</p>
                  </div>
                ) : (
                  <div className="overflow-x-auto">
                    <table className="w-full border-collapse">
                      <thead>
                        <tr className="bg-gray-200">
                          <th className="p-3 text-left">Student ID</th>
                          <th className="p-3 text-left">Name</th>
                          <th className="p-3 text-left">Email</th>
                          <th className="p-3 text-left">Institute</th>
                          <th className="p-3 text-center">Certificates</th>
                          <th className="p-3 text-center">Verifications</th>
                        </tr>
                      </thead>
                      <tbody>
                        {students.map(student => (
                          <tr key={student.id} className="border-b hover:bg-gray-50">
                            <td className="p-3 font-mono text-sm">{student.student_id}</td>
                            <td className="p-3 font-semibold">{student.name}</td>
                            <td className="p-3 text-sm">{student.email}</td>
                            <td className="p-3 text-sm">{student.institute_name}</td>
                            <td className="p-3 text-center">{student.certificate_count}</td>
                            <td className="p-3 text-center">{student.verification_count}</td>
                          </tr>
                        ))}
                      </tbody>
                    </table>
                  </div>
                )}
              </div>
            )}

            {/* MODULE 5: Manage Verifiers */}
            {activeModule === 'verifiers' && !loading && (
              <div>
                <div className="flex justify-between items-center mb-6">
                  <h2 className="text-3xl font-bold text-gray-800">Manage Verifiers</h2>
                  <button
                    onClick={() => setShowVerifierForm(true)}
                    className="bg-blue-500 text-white px-6 py-2 rounded-lg hover:bg-blue-600 font-semibold"
                  >
                    + Add Verifier
                  </button>
                </div>

                {showVerifierForm && (
                  <div className="mb-6 bg-gray-50 p-6 rounded-lg border">
                    <h3 className="font-bold text-lg mb-4">Add New Verifier</h3>
                    <form onSubmit={addVerifier} className="space-y-4">
                      <div>
                        <label className="block font-semibold mb-2">Username *</label>
                        <input
                          type="text"
                          required
                          className="w-full px-4 py-2 border rounded-lg"
                          value={formData.username || ''}
                          onChange={(e) => setFormData({...formData, username: e.target.value})}
                        />
                      </div>
                      <div>
                        <label className="block font-semibold mb-2">Email *</label>
                        <input
                          type="email"
                          required
                          className="w-full px-4 py-2 border rounded-lg"
                          value={formData.email || ''}
                          onChange={(e) => setFormData({...formData, email: e.target.value})}
                        />
                      </div>
                      <div>
                        <label className="block font-semibold mb-2">Password *</label>
                        <input
                          type="password"
                          required
                          minLength="6"
                          className="w-full px-4 py-2 border rounded-lg"
                          value={formData.password || ''}
                          onChange={(e) => setFormData({...formData, password: e.target.value})}
                        />
                      </div>
                      <div className="flex gap-2">
                        <button type="submit" className="bg-green-500 text-white px-6 py-2 rounded-lg hover:bg-green-600">
                          Create Verifier
                        </button>
                        <button
                          type="button"
                          onClick={() => {setShowVerifierForm(false); setFormData({});}}
                          className="bg-gray-500 text-white px-6 py-2 rounded-lg hover:bg-gray-600"
                        >
                          Cancel
                        </button>
                      </div>
                    </form>
                  </div>
                )}
                <div className="overflow-x-auto">
                  <table className="w-full border-collapse">
                    <thead>
                      <tr className="bg-gray-200">
                        <th className="p-3 text-left">Username</th>
                        <th className="p-3 text-left">Company</th>
                        <th className="p-3 text-left">Email</th>
                        <th className="p-3 text-center">Type</th>
                        <th className="p-3 text-center">Verifications</th>
                        <th className="p-3 text-center">Status</th>
                        <th className="p-3 text-center">Actions</th>
                      </tr>
                    </thead>
                    <tbody>
                      {verifiers.map(verifier => (
                        <tr key={verifier.id} className="border-b hover:bg-gray-50">
                          <td className="p-3 font-semibold">{verifier.username}</td>
                          <td className="p-3">{verifier.company_name || 'N/A'}</td>
                          <td className="p-3 text-sm">{verifier.email}</td>
                          <td className="p-3 text-center text-sm">{verifier.verifier_type}</td>
                          <td className="p-3 text-center font-semibold">{verifier.verification_count}</td>
                          <td className="p-3 text-center">
                            <span className={`px-2 py-1 rounded text-xs ${
                              verifier.status === 'active' ? 'bg-green-100 text-green-800' : 'bg-gray-100 text-gray-800'
                            }`}>
                              {verifier.status}
                            </span>
                          </td>
                          <td className="p-3 text-center">
                            <button 
                              onClick={() => deleteVerifier(verifier.id)} 
                              className="text-red-500 hover:text-red-700 font-semibold"
                            >
                              Delete
                            </button>
                          </td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              </div>
            )}

            {/* MODULE 6: Monitor Verifications */}
            {activeModule === 'verifications' && !loading && (
              <div>
                <h2 className="text-3xl font-bold mb-6 text-gray-800">Monitor Verifications</h2>
                <div className="overflow-x-auto">
                  <table className="w-full border-collapse text-sm">
                    <thead>
                      <tr className="bg-gray-200">
                        <th className="p-3 text-left">Verification ID</th>
                        <th className="p-3 text-left">Verifier</th>
                        <th className="p-3 text-center">Result</th>
                        <th className="p-3 text-center">Status</th>
                        <th className="p-3 text-center">Confidence</th>
                        <th className="p-3 text-center">Suspicious</th>
                        <th className="p-3 text-center">Actions</th>
                      </tr>
                    </thead>
                    <tbody>
                      {verifications.map(verif => (
                        <tr key={verif.id} className="border-b hover:bg-gray-50">
                          <td className="p-3 font-mono text-xs">{verif.id.slice(0, 12)}...</td>
                          <td className="p-3">{verif.verifier_id}</td>
                          <td className="p-3 text-center">
                            <span className={`px-2 py-1 rounded text-xs ${
                              verif.result ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'
                            }`}>
                              {verif.result ? 'Valid' : 'Invalid'}
                            </span>
                          </td>
                          <td className="p-3 text-center">{verif.status}</td>
                          <td className="p-3 text-center">{verif.confidence_score ? `${(verif.confidence_score * 100).toFixed(1)}%` : 'N/A'}</td>
                          <td className="p-3 text-center">
                            {verif.is_suspicious ? '🚨 Yes' : '✅ No'}
                          </td>
                          <td className="p-3 text-center">
                            {!verif.is_suspicious && (
                              <button 
                                onClick={() => flagVerification(verif.id)} 
                                className="text-orange-500 hover:text-orange-700 font-semibold"
                              >
                                Flag
                              </button>
                            )}
                          </td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              </div>
            )}

            {/* MODULE 7: Generate Reports */}
            {activeModule === 'reports' && !loading && (
              <div>
                <h2 className="text-3xl font-bold mb-6 text-gray-800">AI-Powered Reports</h2>
                <p className="text-gray-600 mb-6">Generate comprehensive reports with AI insights and visual analytics</p>
                
                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                  <div className="bg-blue-50 p-6 rounded-lg border border-blue-200">
                    <h3 className="font-bold text-lg mb-2">📊 Institute Report</h3>
                    <p className="text-sm text-gray-600 mb-4">AI-powered analysis of institute performance with student and certificate metrics</p>
                    <button 
                      onClick={() => generateReport('institute')}
                      className="bg-blue-500 text-white px-6 py-2 rounded-lg w-full hover:bg-blue-600 transition"
                    >
                      Generate AI Report
                    </button>
                  </div>
                  
                  <div className="bg-green-50 p-6 rounded-lg border border-green-200">
                    <h3 className="font-bold text-lg mb-2">📜 Certificate Report</h3>
                    <p className="text-sm text-gray-600 mb-4">Detailed certificate analytics with AI insights on issuance patterns and status</p>
                    <button 
                      onClick={() => generateReport('certificates')}
                      className="bg-green-500 text-white px-6 py-2 rounded-lg w-full hover:bg-green-600 transition"
                    >
                      Generate AI Report
                    </button>
                  </div>
                  
                  <div className="bg-purple-50 p-6 rounded-lg border border-purple-200">
                    <h3 className="font-bold text-lg mb-2">✅ Verification Report</h3>
                    <p className="text-sm text-gray-600 mb-4">AI analysis of verification success rates and security patterns</p>
                    <button 
                      onClick={() => generateReport('verifications')}
                      className="bg-purple-500 text-white px-6 py-2 rounded-lg w-full hover:bg-purple-600 transition"
                    >
                      Generate AI Report
                    </button>
                  </div>
                  
                  <div className="bg-orange-50 p-6 rounded-lg border border-orange-200">
                    <h3 className="font-bold text-lg mb-2">📈 System Activity Report</h3>
                    <p className="text-sm text-gray-600 mb-4">Complete system overview with AI-powered performance insights</p>
                    <button 
                      onClick={() => generateReport('system')}
                      className="bg-orange-500 text-white px-6 py-2 rounded-lg w-full hover:bg-orange-600 transition"
                    >
                      Generate AI Report
                    </button>
                  </div>
                </div>
                
                <div className="mt-8 bg-yellow-50 p-6 rounded-lg border border-yellow-200">
                  <h3 className="font-bold text-lg mb-2">🤖 AI Features</h3>
                  <ul className="text-sm text-gray-700 space-y-1">
                    <li>• Executive summaries with key insights</li>
                    <li>• System health analysis and risk indicators</li>
                    <li>• Professional charts and visualizations</li>
                    <li>• Downloadable reports and images</li>
                  </ul>
                </div>
              </div>
            )}

            {/* MODULE 8: Feedback Management */}
            {activeModule === 'feedback' && !loading && (
              <div>
                <h2 className="text-3xl font-bold mb-6 text-gray-800">Feedback Management</h2>
                <div className="overflow-x-auto">
                  <table className="w-full border-collapse">
                    <thead>
                      <tr className="bg-gray-200">
                        <th className="p-3 text-left">Feedback ID</th>
                        <th className="p-3 text-left">Verifier</th>
                        <th className="p-3 text-left">Message</th>
                        <th className="p-3 text-center">Category</th>
                        <th className="p-3 text-center">Priority</th>
                        <th className="p-3 text-center">Status</th>
                        <th className="p-3 text-center">Actions</th>
                      </tr>
                    </thead>
                    <tbody>
                      {feedbacks.map(fb => (
                        <tr key={fb.id} className="border-b hover:bg-gray-50">
                          <td className="p-3 font-mono text-xs">{fb.id.slice(0, 12)}...</td>
                          <td className="p-3">{fb.verifier_id}</td>
                          <td className="p-3 text-sm">{fb.message.slice(0, 60)}...</td>
                          <td className="p-3 text-center text-xs">{fb.category}</td>
                          <td className="p-3 text-center">
                            <span className={`px-2 py-1 rounded text-xs ${
                              fb.priority === 'high' ? 'bg-red-100 text-red-800' :
                              fb.priority === 'medium' ? 'bg-yellow-100 text-yellow-800' :
                              'bg-green-100 text-green-800'
                            }`}>
                              {fb.priority}
                            </span>
                          </td>
                          <td className="p-3 text-center text-xs">{fb.status}</td>
                          <td className="p-3 text-center">
                            {!fb.flagged && (
                              <button 
                                onClick={() => flagFeedback(fb.id)} 
                                className="text-orange-500 hover:text-orange-700 font-semibold"
                              >
                                Flag
                              </button>
                            )}
                            {fb.flagged && <span className="text-orange-600">🚩 Flagged</span>}
                          </td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              </div>
            )}
          </div>
        </div>
      </div>
      
      {/* Report Dialog */}
      <ReportDialog
        isOpen={showReportDialog}
        onClose={() => {
          setShowReportDialog(false);
          setReportData(null);
          setReportType('');
        }}
        reportData={reportData}
        reportType={reportType}
        loading={reportLoading}
      />
    </div>
  );
};

export default AdminDashboard;
