import React, { useState, useEffect } from 'react';
import axios from 'axios';

const API_URL = 'http://localhost:8000/api/institute';

const InstituteDashboardEnhanced = () => {
  const [activeModule, setActiveModule] = useState('dashboard');
  const [dashboardStats, setDashboardStats] = useState(null);
  const [students, setStudents] = useState([]);
  const [certificates, setCertificates] = useState([]);
  const [tracking, setTracking] = useState(null);
  const [analysis, setAnalysis] = useState(null);
  const [feedback, setFeedback] = useState([]);
  const [report, setReport] = useState(null);
  const [loading, setLoading] = useState(false);

  const token = localStorage.getItem('token');
  const headers = { Authorization: `Bearer ${token}` };

  useEffect(() => {
    if (activeModule === 'dashboard') loadDashboard();
    else if (activeModule === 'students') loadStudents();
    else if (activeModule === 'certificates') loadCertificates();
    else if (activeModule === 'track') loadTracking();
    else if (activeModule === 'analysis') loadAnalysis();
    else if (activeModule === 'feedback') loadFeedback();
  }, [activeModule]);

  const loadDashboard = async () => {
    try {
      const res = await axios.get(`${API_URL}/dashboard`, { headers });
      setDashboardStats(res.data);
    } catch (err) {
      console.error(err);
    }
  };

  const loadStudents = async () => {
    setLoading(true);
    try {
      const res = await axios.get(`${API_URL}/students`, { headers });
      setStudents(res.data.students);
    } catch (err) {
      console.error(err);
    }
    setLoading(false);
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

  const loadTracking = async () => {
    try {
      const res = await axios.get(`${API_URL}/certificates/track`, { headers });
      setTracking(res.data);
    } catch (err) {
      console.error(err);
    }
  };

  const loadAnalysis = async () => {
    try {
      const res = await axios.get(`${API_URL}/analysis`, { headers });
      setAnalysis(res.data);
    } catch (err) {
      console.error(err);
    }
  };

  const loadFeedback = async () => {
    try {
      const res = await axios.get(`${API_URL}/feedback`, { headers });
      setFeedback(res.data.feedbacks);
    } catch (err) {
      console.error(err);
    }
  };

  const addStudent = async (e) => {
    e.preventDefault();
    const formData = new FormData(e.target);
    
    try {
      await axios.post(
        `${API_URL}/students?name=${encodeURIComponent(formData.get('name'))}&email=${encodeURIComponent(formData.get('email'))}&password=${encodeURIComponent(formData.get('password'))}`,
        {},
        { headers }
      );
      alert('✅ Student added successfully');
      e.target.reset();
      loadStudents();
      loadDashboard();
    } catch (err) {
      alert('❌ Error adding student');
    }
  };

  const updateStudent = async (studentId, name, email, phone) => {
    try {
      await axios.put(
        `${API_URL}/students/${studentId}?name=${encodeURIComponent(name)}&email=${encodeURIComponent(email)}&phone=${phone || ''}`,
        {},
        { headers }
      );
      alert('✅ Student updated successfully');
      loadStudents();
    } catch (err) {
      alert('❌ Error updating student');
    }
  };

  const removeStudent = async (studentId) => {
    if (!confirm('Are you sure you want to remove this student?')) return;
    
    try {
      await axios.delete(`${API_URL}/students/${studentId}`, { headers });
      alert('✅ Student removed successfully');
      loadStudents();
      loadDashboard();
    } catch (err) {
      alert('❌ Error removing student');
    }
  };

  const issueCertificate = async (e) => {
    e.preventDefault();
    const formData = new FormData(e.target);
    
    try {
      await axios.post(`${API_URL}/certificates/issue?student_id=${formData.get('student_id')}`, formData, { headers });
      alert('✅ Certificate issued successfully');
      e.target.reset();
      loadCertificates();
      loadDashboard();
    } catch (err) {
      alert('❌ Error issuing certificate');
    }
  };

  const generateReport = async (reportType) => {
    try {
      const res = await axios.get(`${API_URL}/reports/${reportType}`, { headers });
      setReport(res.data);
      alert(`✅ ${res.data.report_type} generated`);
    } catch (err) {
      alert('❌ Error generating report');
    }
  };

  const handleLogout = () => {
    localStorage.removeItem('token');
    window.location.href = '/';
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-50 to-indigo-50">
      {/* Navigation */}
      <nav className="bg-gradient-to-r from-indigo-600 to-indigo-700 text-white shadow-xl">
        <div className="container mx-auto px-6 py-4 flex justify-between items-center">
          <div>
            <h1 className="text-3xl font-bold">🏫 Institute Portal</h1>
            <p className="text-sm text-indigo-100 mt-1">CertiSense AI v3.0</p>
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
                { id: 'students', label: '👥 Manage Students', desc: 'Add/Edit/Remove' },
                { id: 'certificates', label: '📜 Certificates', desc: 'View All' },
                { id: 'issue', label: '✅ Issue Certificate', desc: 'New Certificate' },
                { id: 'track', label: '🔍 Track Certificates', desc: 'Verification Activity' },
                { id: 'analysis', label: '📈 System Analysis', desc: 'Analytics' },
                { id: 'reports', label: '📄 Generate Reports', desc: 'Export Data' },
                { id: 'feedback', label: '💬 Feedback', desc: 'View Feedback' }
              ].map(mod => (
                <li key={mod.id}>
                  <button
                    onClick={() => setActiveModule(mod.id)}
                    className={`w-full text-left px-4 py-3 rounded-lg transition shadow-sm ${
                      activeModule === mod.id 
                        ? 'bg-gradient-to-r from-indigo-500 to-indigo-600 text-white shadow-lg transform scale-105' 
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
                <h2 className="text-4xl font-bold mb-8 text-gray-800">📊 Institute Dashboard</h2>
                
                <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                  <div className="bg-gradient-to-br from-blue-400 to-blue-600 text-white p-6 rounded-xl shadow-lg">
                    <h3 className="text-sm font-semibold mb-2 opacity-90">Total Students</h3>
                    <p className="text-5xl font-bold">{dashboardStats.statistics.total_students}</p>
                  </div>
                  <div className="bg-gradient-to-br from-green-400 to-green-600 text-white p-6 rounded-xl shadow-lg">
                    <h3 className="text-sm font-semibold mb-2 opacity-90">Certificates Issued</h3>
                    <p className="text-5xl font-bold">{dashboardStats.statistics.total_certificates}</p>
                  </div>
                  <div className="bg-gradient-to-br from-purple-400 to-purple-600 text-white p-6 rounded-xl shadow-lg">
                    <h3 className="text-sm font-semibold mb-2 opacity-90">Verifications</h3>
                    <p className="text-5xl font-bold">{dashboardStats.statistics.total_verifications}</p>
                  </div>
                </div>

                <div className="mt-8 bg-gradient-to-r from-indigo-50 to-purple-50 p-6 rounded-xl border border-indigo-200">
                  <h3 className="font-bold text-lg mb-4">🏫 Institute Information</h3>
                  <div className="space-y-2">
                    <p><strong>Name:</strong> {dashboardStats.institute_info.name}</p>
                    <p><strong>Institute ID:</strong> {dashboardStats.institute_info.institute_id}</p>
                    <p><strong>Email:</strong> {dashboardStats.institute_info.email}</p>
                  </div>
                </div>
              </div>
            )}

            {/* Students Module */}
            {activeModule === 'students' && (
              <div>
                <h2 className="text-4xl font-bold mb-8 text-gray-800">👥 Manage Students</h2>
                
                <form onSubmit={addStudent} className="mb-8 bg-gradient-to-r from-blue-50 to-indigo-50 p-6 rounded-xl border-2 border-blue-200 space-y-4">
                  <h3 className="font-bold text-lg">Add New Student</h3>
                  <input name="name" placeholder="Full Name" className="w-full px-4 py-3 border-2 border-gray-300 rounded-lg" required />
                  <input name="email" type="email" placeholder="Email" className="w-full px-4 py-3 border-2 border-gray-300 rounded-lg" required />
                  <input name="password" type="password" placeholder="Password" className="w-full px-4 py-3 border-2 border-gray-300 rounded-lg" required />
                  <button type="submit" className="w-full bg-blue-600 text-white px-6 py-3 rounded-lg hover:bg-blue-700 font-semibold shadow-md">
                    ➕ Add Student
                  </button>
                </form>

                {loading ? (
                  <div className="text-center py-12">Loading...</div>
                ) : (
                  <div className="space-y-3">
                    {students.map(s => (
                      <div key={s.id} className="border-2 border-gray-200 p-4 rounded-xl hover:shadow-lg transition">
                        <div className="flex justify-between items-start">
                          <div>
                            <p className="font-bold text-lg">{s.name}</p>
                            <p className="text-sm text-gray-600">ID: {s.student_id}</p>
                            <p className="text-sm text-gray-600">Email: {s.email}</p>
                            <p className="text-sm text-gray-600">Status: <span className="text-green-600 font-semibold">{s.status}</span></p>
                          </div>
                          <div className="flex gap-2">
                            <button onClick={() => removeStudent(s.id)} className="bg-red-500 text-white px-4 py-2 rounded-lg hover:bg-red-600 text-sm">
                              🗑️ Remove
                            </button>
                          </div>
                        </div>
                      </div>
                    ))}
                  </div>
                )}
              </div>
            )}

            {/* Certificates Module */}
            {activeModule === 'certificates' && (
              <div>
                <h2 className="text-4xl font-bold mb-8 text-gray-800">📜 Manage Certificates</h2>
                
                {loading ? (
                  <div className="text-center py-12">Loading...</div>
                ) : (
                  <div className="overflow-x-auto rounded-xl border-2 border-gray-200">
                    <table className="w-full">
                      <thead className="bg-gradient-to-r from-gray-100 to-gray-200">
                        <tr>
                          <th className="p-4 text-left font-bold">Certificate Title</th>
                          <th className="p-4 text-left font-bold">Student</th>
                          <th className="p-4 text-center font-bold">Status</th>
                          <th className="p-4 text-center font-bold">Verifications</th>
                          <th className="p-4 text-left font-bold">Issue Date</th>
                        </tr>
                      </thead>
                      <tbody>
                        {certificates.map((c, idx) => (
                          <tr key={idx} className={`border-b hover:bg-gray-50 ${idx % 2 === 0 ? 'bg-white' : 'bg-gray-50'}`}>
                            <td className="p-4">{c.certificate_title}</td>
                            <td className="p-4 text-sm">{c.student_name} ({c.student_id})</td>
                            <td className="p-4 text-center">
                              <span className={`px-3 py-1 rounded-lg text-xs font-bold ${
                                c.status === 'active' ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'
                              }`}>
                                {c.status}
                              </span>
                            </td>
                            <td className="p-4 text-center font-semibold">{c.verification_count}</td>
                            <td className="p-4 text-sm">{c.issue_date ? new Date(c.issue_date).toLocaleDateString() : 'N/A'}</td>
                          </tr>
                        ))}
                      </tbody>
                    </table>
                  </div>
                )}
              </div>
            )}

            {/* Issue Certificate Module */}
            {activeModule === 'issue' && (
              <div>
                <h2 className="text-4xl font-bold mb-8 text-gray-800">✅ Issue Certificate</h2>
                
                <form onSubmit={issueCertificate} className="bg-gradient-to-r from-green-50 to-emerald-50 p-8 rounded-xl border-2 border-green-200 space-y-6">
                  <div>
                    <label className="block font-bold mb-2">Select Student</label>
                    <select name="student_id" className="w-full px-4 py-3 border-2 border-gray-300 rounded-lg" required>
                      <option value="">Choose student...</option>
                      {students.map(s => (
                        <option key={s.id} value={s.student_id}>{s.name} ({s.student_id})</option>
                      ))}
                    </select>
                  </div>

                  <div>
                    <label className="block font-bold mb-2">Certificate File</label>
                    <input name="file" type="file" accept=".pdf,.jpg,.png" className="w-full px-4 py-3 border-2 border-gray-300 rounded-lg" required />
                  </div>

                  <button type="submit" className="w-full bg-green-600 text-white px-6 py-4 rounded-lg hover:bg-green-700 font-bold text-lg shadow-lg">
                    🎓 Issue Certificate
                  </button>
                </form>
              </div>
            )}

            {/* Track Certificates Module */}
            {activeModule === 'track' && tracking && (
              <div>
                <h2 className="text-4xl font-bold mb-8 text-gray-800">🔍 Track Certificates</h2>
                
                <div className="grid grid-cols-3 gap-4 mb-8">
                  <div className="bg-blue-50 p-4 rounded-xl border border-blue-200">
                    <p className="text-sm text-gray-600">Total Certificates</p>
                    <p className="text-3xl font-bold text-blue-600">{tracking.total_certificates}</p>
                  </div>
                  <div className="bg-green-50 p-4 rounded-xl border border-green-200">
                    <p className="text-sm text-gray-600">Total Verifications</p>
                    <p className="text-3xl font-bold text-green-600">{tracking.total_verifications}</p>
                  </div>
                  <div className="bg-red-50 p-4 rounded-xl border border-red-200">
                    <p className="text-sm text-gray-600">Suspicious Activity</p>
                    <p className="text-3xl font-bold text-red-600">{tracking.suspicious_activity_count}</p>
                  </div>
                </div>

                <div className="overflow-x-auto rounded-xl border-2 border-gray-200">
                  <table className="w-full">
                    <thead className="bg-gradient-to-r from-gray-100 to-gray-200">
                      <tr>
                        <th className="p-4 text-left font-bold">Certificate</th>
                        <th className="p-4 text-left font-bold">Verifier ID</th>
                        <th className="p-4 text-center font-bold">Status</th>
                        <th className="p-4 text-left font-bold">Date</th>
                      </tr>
                    </thead>
                    <tbody>
                      {tracking.verifications.map((v, idx) => (
                        <tr key={idx} className={`border-b hover:bg-gray-50 ${v.is_suspicious ? 'bg-red-50' : ''}`}>
                          <td className="p-4">{v.certificate_name}</td>
                          <td className="p-4 text-sm font-mono">{v.verifier_id.substring(0, 12)}...</td>
                          <td className="p-4 text-center">
                            <span className={`px-3 py-1 rounded-lg text-xs font-bold ${
                              v.result ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'
                            }`}>
                              {v.verification_status}
                            </span>
                          </td>
                          <td className="p-4 text-sm">{new Date(v.timestamp).toLocaleString()}</td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              </div>
            )}

            {/* Analysis Module */}
            {activeModule === 'analysis' && analysis && (
              <div>
                <h2 className="text-4xl font-bold mb-8 text-gray-800">📈 System Analysis</h2>
                
                <div className="grid grid-cols-2 gap-6 mb-8">
                  <div className="bg-gradient-to-br from-blue-400 to-blue-600 text-white p-6 rounded-xl shadow-lg">
                    <h3 className="text-sm font-semibold mb-2 opacity-90">Students Registered</h3>
                    <p className="text-5xl font-bold">{analysis.total_students_registered}</p>
                  </div>
                  <div className="bg-gradient-to-br from-green-400 to-green-600 text-white p-6 rounded-xl shadow-lg">
                    <h3 className="text-sm font-semibold mb-2 opacity-90">Certificates Issued</h3>
                    <p className="text-5xl font-bold">{analysis.total_certificates_issued}</p>
                  </div>
                  <div className="bg-gradient-to-br from-purple-400 to-purple-600 text-white p-6 rounded-xl shadow-lg">
                    <h3 className="text-sm font-semibold mb-2 opacity-90">Verification Requests</h3>
                    <p className="text-5xl font-bold">{analysis.total_verification_requests}</p>
                  </div>
                  <div className="bg-gradient-to-br from-orange-400 to-orange-600 text-white p-6 rounded-xl shadow-lg">
                    <h3 className="text-sm font-semibold mb-2 opacity-90">Success Rate</h3>
                    <p className="text-5xl font-bold">{analysis.verification_success_rate}%</p>
                  </div>
                </div>

                <div className="bg-gradient-to-r from-indigo-50 to-purple-50 p-6 rounded-xl border border-indigo-200">
                  <h3 className="font-bold text-lg mb-4">📊 Analytics</h3>
                  <div className="grid grid-cols-2 gap-4">
                    <div>
                      <p className="text-sm text-gray-600">Avg Verifications/Certificate</p>
                      <p className="text-2xl font-bold text-indigo-600">{analysis.analytics.avg_verifications_per_certificate}</p>
                    </div>
                    <div>
                      <p className="text-sm text-gray-600">Active Certificates</p>
                      <p className="text-2xl font-bold text-purple-600">{analysis.analytics.active_certificates}</p>
                    </div>
                  </div>
                </div>
              </div>
            )}

            {/* Reports Module */}
            {activeModule === 'reports' && (
              <div>
                <h2 className="text-4xl font-bold mb-8 text-gray-800">📄 Generate Reports</h2>
                
                <div className="grid grid-cols-3 gap-4 mb-8">
                  <button onClick={() => generateReport('student')} className="bg-blue-500 text-white px-6 py-4 rounded-xl hover:bg-blue-600 font-semibold shadow-lg">
                    📋 Student Report
                  </button>
                  <button onClick={() => generateReport('certificate')} className="bg-green-500 text-white px-6 py-4 rounded-xl hover:bg-green-600 font-semibold shadow-lg">
                    📜 Certificate Report
                  </button>
                  <button onClick={() => generateReport('verification')} className="bg-purple-500 text-white px-6 py-4 rounded-xl hover:bg-purple-600 font-semibold shadow-lg">
                    🔍 Verification Report
                  </button>
                </div>

                {report && (
                  <div className="bg-gray-50 p-6 rounded-xl border-2 border-gray-200">
                    <h3 className="font-bold text-xl mb-4">{report.report_type}</h3>
                    <p className="text-sm text-gray-600 mb-4">Period: {report.period}</p>
                    <p className="text-lg font-semibold mb-4">Total Records: {report.data.length}</p>
                    <pre className="bg-white p-4 rounded border overflow-auto max-h-96 text-xs">
                      {JSON.stringify(report.data, null, 2)}
                    </pre>
                  </div>
                )}
              </div>
            )}

            {/* Feedback Module */}
            {activeModule === 'feedback' && (
              <div>
                <h2 className="text-4xl font-bold mb-8 text-gray-800">💬 Feedback Management</h2>
                
                {feedback.length === 0 ? (
                  <div className="text-center py-12 text-gray-600">No feedback received yet</div>
                ) : (
                  <div className="space-y-4">
                    {feedback.map(fb => (
                      <div key={fb.feedback_id} className={`p-6 rounded-xl border-2 ${fb.flagged ? 'bg-red-50 border-red-200' : 'bg-gray-50 border-gray-200'}`}>
                        <div className="flex justify-between items-start mb-3">
                          <div>
                            <p className="font-bold text-lg">{fb.category}</p>
                            <p className="text-sm text-gray-600">Certificate: {fb.certificate_name}</p>
                          </div>
                          <span className={`px-3 py-1 rounded-lg text-xs font-bold ${
                            fb.flagged ? 'bg-red-100 text-red-800' : 'bg-green-100 text-green-800'
                          }`}>
                            {fb.status}
                          </span>
                        </div>
                        <p className="text-gray-700 mb-3">{fb.message}</p>
                        <p className="text-xs text-gray-500">{new Date(fb.timestamp).toLocaleString()}</p>
                      </div>
                    ))}
                  </div>
                )}
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default InstituteDashboardEnhanced;
