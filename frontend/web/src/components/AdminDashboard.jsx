import React, { useState, useEffect } from 'react';
import axios from 'axios';
import ReportDialog from './ReportDialog';
import AIAssistantWidget from './AIAssistantWidget';
import Layout from './Layout';
import { StatCard, InfoCard, Button, Badge } from './UIComponents';

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

  const navigationItems = [
    { id: 'dashboard', label: 'Dashboard' },
    { id: 'institutes', label: 'Institutes' },
    { id: 'certificates', label: 'Certificates' },
    { id: 'students', label: 'Students' },
    { id: 'verifiers', label: 'Verifiers' },
    { id: 'verifications', label: 'Verifications' },
    { id: 'reports', label: 'Reports' },
    { id: 'feedback', label: 'Feedback' }
  ];

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
    <>
      <Layout
        title="CertiSense AI v3.0"
        subtitle="Admin Control System"
        userRole="Administrator"
        onLogout={handleLogout}
        navigationItems={navigationItems}
        activeModule={activeModule}
        onModuleChange={setActiveModule}
        themeColor="blue"
      >
        <div>
        {loading && (
          <div className="flex items-center justify-center py-12">
            <div className="text-center">
              <div className="loading-spinner mx-auto mb-4"></div>
              <p className="text-secondary-600">Loading...</p>
            </div>
          </div>
        )}

        {/* MODULE 1: Dashboard Analytics */}
            {activeModule === 'dashboard' && analytics && !loading && (
              <div className="space-y-6">
                <div className="mb-6">
                  <h2 className="text-2xl font-bold text-secondary-800 mb-2">System Analytics</h2>
                  <p className="text-secondary-600">Overview of system performance and metrics</p>
                </div>
                
                {/* Key Metrics */}
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
                  <StatCard 
                    title="Total Institutes"
                    value={analytics.total_institutes}
                    icon="fa-building-columns"
                    color="blue"
                  />
                  <StatCard 
                    title="Total Students"
                    value={analytics.total_students}
                    icon="fa-user-graduate"
                    color="green"
                  />
                  <StatCard 
                    title="Total Certificates"
                    value={analytics.total_certificates}
                    icon="fa-certificate"
                    color="yellow"
                  />
                  <StatCard 
                    title="Total Verifications"
                    value={analytics.total_verifications}
                    icon="fa-check-double"
                    color="purple"
                  />
                </div>

                {/* Performance Metrics */}
                <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                  <InfoCard title="Verification Success Rate">
                    <div className="flex items-center justify-between">
                      <div>
                        <div className="text-5xl font-bold text-green-600 mb-2">{analytics.verification_success_rate}%</div>
                        <p className="text-secondary-600">Successful verifications</p>
                        <p className="text-sm text-secondary-500 mt-1">System performance indicator</p>
                      </div>
                      <div className="text-6xl text-green-500 opacity-20">
                        <i className="fas fa-chart-line"></i>
                      </div>
                    </div>
                  </InfoCard>

                  <InfoCard title="Certificate Status Distribution">
                    <div className="space-y-3">
                      <div className="flex items-center justify-between p-3 bg-green-50 rounded-lg">
                        <div className="flex items-center gap-2">
                          <div className="w-3 h-3 rounded-full bg-green-500"></div>
                          <span className="font-medium text-secondary-700">Active</span>
                        </div>
                        <span className="text-2xl font-bold text-green-600">{analytics.certificate_status.active}</span>
                      </div>
                      <div className="flex items-center justify-between p-3 bg-red-50 rounded-lg">
                        <div className="flex items-center gap-2">
                          <div className="w-3 h-3 rounded-full bg-red-500"></div>
                          <span className="font-medium text-secondary-700">Revoked</span>
                        </div>
                        <span className="text-2xl font-bold text-red-600">{analytics.certificate_status.revoked}</span>
                      </div>
                      <div className="flex items-center justify-between p-3 bg-orange-50 rounded-lg">
                        <div className="flex items-center gap-2">
                          <div className="w-3 h-3 rounded-full bg-orange-500"></div>
                          <span className="font-medium text-secondary-700">Suspicious</span>
                        </div>
                        <span className="text-2xl font-bold text-orange-600">{analytics.certificate_status.suspicious}</span>
                      </div>
                    </div>
                  </InfoCard>
                </div>

                {/* Recent Activity */}
                <InfoCard title="Recent Activity (30 Days)">
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                    <div className="flex items-center gap-4 p-4 bg-blue-50 rounded-lg">
                      <div className="w-12 h-12 rounded-full bg-blue-100 flex items-center justify-center">
                        <i className="fas fa-file-certificate text-blue-600 text-xl"></i>
                      </div>
                      <div>
                        <p className="text-sm text-secondary-600">New Certificates</p>
                        <p className="text-2xl font-bold text-blue-600">{analytics.recent_certificates_30d}</p>
                      </div>
                    </div>
                    <div className="flex items-center gap-4 p-4 bg-purple-50 rounded-lg">
                      <div className="w-12 h-12 rounded-full bg-purple-100 flex items-center justify-center">
                        <i className="fas fa-check-circle text-purple-600 text-xl"></i>
                      </div>
                      <div>
                        <p className="text-sm text-secondary-600">New Verifications</p>
                        <p className="text-2xl font-bold text-purple-600">{analytics.recent_verifications_30d}</p>
                      </div>
                    </div>
                  </div>
                </InfoCard>
              </div>
            )}

            {/* MODULE 2: Manage Institutes */}
            {activeModule === 'institutes' && !loading && (
              <div className="space-y-6">
                <div className="flex justify-between items-center">
                  <div>
                    <h2 className="text-2xl font-bold text-secondary-800">Manage Institutes</h2>
                    <p className="text-secondary-600 text-sm mt-1">View and manage all registered institutes</p>
                  </div>
                  <Button 
                    onClick={() => setShowInstituteForm(true)}
                    icon="fa-plus"
                  >
                    Add Institute
                  </Button>
                </div>

                {showInstituteForm && (
                  <InfoCard title="Add New Institute">
                    <form onSubmit={addInstitute} className="space-y-4">
                      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                        <div>
                          <label className="block font-medium mb-2">Institute Name *</label>
                          <input
                            type="text"
                            required
                            className="w-full"
                            value={formData.name || ''}
                            onChange={(e) => setFormData({...formData, name: e.target.value})}
                          />
                        </div>
                        <div>
                          <label className="block font-medium mb-2">Email *</label>
                          <input
                            type="email"
                            required
                            className="w-full"
                            value={formData.email || ''}
                            onChange={(e) => setFormData({...formData, email: e.target.value})}
                          />
                        </div>
                        <div>
                          <label className="block font-medium mb-2">Password *</label>
                          <input
                            type="password"
                            required
                            minLength="6"
                            className="w-full"
                            value={formData.password || ''}
                            onChange={(e) => setFormData({...formData, password: e.target.value})}
                          />
                        </div>
                        <div>
                          <label className="block font-medium mb-2">Location</label>
                          <input
                            type="text"
                            className="w-full"
                            value={formData.location || ''}
                            onChange={(e) => setFormData({...formData, location: e.target.value})}
                          />
                        </div>
                      </div>
                      <div className="flex gap-2 pt-4">
                        <Button type="submit" variant="success" icon="fa-check">
                          Create Institute
                        </Button>
                        <Button 
                          type="button" 
                          variant="secondary"
                          onClick={() => {setShowInstituteForm(false); setFormData({});}}
                        >
                          Cancel
                        </Button>
                      </div>
                    </form>
                  </InfoCard>
                )}
                
                <InfoCard>
                  <div className="table-container">
                    <table>
                      <thead>
                        <tr>
                          <th>Institute ID</th>
                          <th>Name</th>
                          <th>Email</th>
                          <th>Location</th>
                          <th className="text-center">Students</th>
                          <th className="text-center">Certificates</th>
                          <th className="text-center">Status</th>
                          <th className="text-center">Actions</th>
                        </tr>
                      </thead>
                      <tbody>
                        {institutes.map(inst => (
                          <tr key={inst.id}>
                            <td className="font-mono text-xs">{inst.institute_id}</td>
                            <td className="font-semibold">{inst.name}</td>
                            <td>{inst.email}</td>
                            <td>{inst.location || 'N/A'}</td>
                            <td className="text-center">
                              <Badge variant="info">{inst.student_count}</Badge>
                            </td>
                            <td className="text-center">
                              <Badge variant="success">{inst.certificate_count}</Badge>
                            </td>
                            <td className="text-center">
                              <Badge variant={inst.approval_status === 'approved' ? 'success' : 'warning'}>
                                {inst.approval_status}
                              </Badge>
                            </td>
                            <td className="text-center">
                              <Button 
                                size="sm" 
                                variant="danger"
                                onClick={() => deleteInstitute(inst.id)}
                              >
                                Delete
                              </Button>
                            </td>
                          </tr>
                        ))}
                      </tbody>
                    </table>
                  </div>
                </InfoCard>
              </div>
            )}

            {/* MODULE 3: Manage Certificates */}
            {activeModule === 'certificates' && !loading && (
              <div className="space-y-6">
                <div>
                  <h2 className="text-2xl font-bold text-secondary-800">Manage Certificates</h2>
                  <p className="text-secondary-600 text-sm mt-1">View all certificates issued in the system</p>
                </div>
                
                {certificates.length === 0 ? (
                  <InfoCard>
                    <div className="text-center py-12">
                      <i className="fas fa-file-certificate text-6xl text-secondary-300 mb-4"></i>
                      <p className="text-secondary-600 text-lg">No certificates found in the system.</p>
                      <p className="text-secondary-500 text-sm mt-2">Certificates will appear here once institutes issue them to students.</p>
                    </div>
                  </InfoCard>
                ) : (
                  <InfoCard>
                    <div className="table-container">
                      <table>
                        <thead>
                          <tr>
                            <th>Certificate ID</th>
                            <th>Student</th>
                            <th>Institute</th>
                            <th className="text-center">Status</th>
                            <th className="text-center">Verifications</th>
                            <th>Issue Date</th>
                          </tr>
                        </thead>
                        <tbody>
                          {certificates.map(cert => (
                            <tr key={cert.id}>
                              <td className="font-mono text-xs">{cert.id.slice(0, 12)}...</td>
                              <td className="font-medium">{cert.student_name}</td>
                              <td>{cert.institute_name}</td>
                              <td className="text-center">
                                <Badge variant={cert.status === 'active' ? 'success' : cert.status === 'revoked' ? 'danger' : 'warning'}>
                                  {cert.status}
                                </Badge>
                              </td>
                              <td className="text-center">
                                <Badge variant="info">{cert.verification_count}</Badge>
                              </td>
                              <td className="text-sm">
                                {cert.issue_date ? new Date(cert.issue_date).toLocaleDateString() : 'N/A'}
                              </td>
                            </tr>
                          ))}
                        </tbody>
                      </table>
                    </div>
                  </InfoCard>
                )}
              </div>
            )}

            {/* MODULE 4: View Students */}
            {activeModule === 'students' && !loading && (
              <div className="space-y-6">
                <div>
                  <h2 className="text-2xl font-bold text-secondary-800">View Students</h2>
                  <p className="text-secondary-600 text-sm mt-1">Read-only view of all students in the system</p>
                </div>
                
                {students.length === 0 ? (
                  <InfoCard>
                    <div className="text-center py-12">
                      <i className="fas fa-user-graduate text-6xl text-secondary-300 mb-4"></i>
                      <p className="text-secondary-600 text-lg">No students found in the system.</p>
                      <p className="text-secondary-500 text-sm mt-2">Students will appear here once institutes add them.</p>
                    </div>
                  </InfoCard>
                ) : (
                  <InfoCard>
                    <div className="table-container">
                      <table>
                        <thead>
                          <tr>
                            <th>Student ID</th>
                            <th>Name</th>
                            <th>Email</th>
                            <th>Institute</th>
                            <th className="text-center">Certificates</th>
                            <th className="text-center">Verifications</th>
                          </tr>
                        </thead>
                        <tbody>
                          {students.map(student => (
                            <tr key={student.id}>
                              <td className="font-mono text-sm">{student.student_id}</td>
                              <td className="font-semibold">{student.name}</td>
                              <td>{student.email}</td>
                              <td>{student.institute_name}</td>
                              <td className="text-center">
                                <Badge variant="success">{student.certificate_count}</Badge>
                              </td>
                              <td className="text-center">
                                <Badge variant="info">{student.verification_count}</Badge>
                              </td>
                            </tr>
                          ))}
                        </tbody>
                      </table>
                    </div>
                  </InfoCard>
                )}
              </div>
            )}

            {/* MODULE 5: Manage Verifiers */}
            {activeModule === 'verifiers' && !loading && (
              <div className="space-y-6">
                <div className="flex justify-between items-center">
                  <div>
                    <h2 className="text-2xl font-bold text-secondary-800">Manage Verifiers</h2>
                    <p className="text-secondary-600 text-sm mt-1">View and manage verification users</p>
                  </div>
                  <Button 
                    onClick={() => setShowVerifierForm(true)}
                    icon="fa-plus"
                  >
                    Add Verifier
                  </Button>
                </div>

                {showVerifierForm && (
                  <InfoCard title="Add New Verifier">
                    <form onSubmit={addVerifier} className="space-y-4">
                      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                        <div>
                          <label className="block font-medium mb-2">Username *</label>
                          <input
                            type="text"
                            required
                            className="w-full"
                            value={formData.username || ''}
                            onChange={(e) => setFormData({...formData, username: e.target.value})}
                          />
                        </div>
                        <div>
                          <label className="block font-medium mb-2">Email *</label>
                          <input
                            type="email"
                            required
                            className="w-full"
                            value={formData.email || ''}
                            onChange={(e) => setFormData({...formData, email: e.target.value})}
                          />
                        </div>
                        <div>
                          <label className="block font-medium mb-2">Password *</label>
                          <input
                            type="password"
                            required
                            minLength="6"
                            className="w-full"
                            value={formData.password || ''}
                            onChange={(e) => setFormData({...formData, password: e.target.value})}
                          />
                        </div>
                      </div>
                      <div className="flex gap-2 pt-4">
                        <Button type="submit" variant="success" icon="fa-check">
                          Create Verifier
                        </Button>
                        <Button 
                          type="button" 
                          variant="secondary"
                          onClick={() => {setShowVerifierForm(false); setFormData({});}}
                        >
                          Cancel
                        </Button>
                      </div>
                    </form>
                  </InfoCard>
                )}
                
                <InfoCard>
                  <div className="table-container">
                    <table>
                      <thead>
                        <tr>
                          <th>Username</th>
                          <th>Company</th>
                          <th>Email</th>
                          <th className="text-center">Type</th>
                          <th className="text-center">Verifications</th>
                          <th className="text-center">Status</th>
                          <th className="text-center">Actions</th>
                        </tr>
                      </thead>
                      <tbody>
                        {verifiers.map(verifier => (
                          <tr key={verifier.id}>
                            <td className="font-semibold">{verifier.username}</td>
                            <td>{verifier.company_name || 'N/A'}</td>
                            <td>{verifier.email}</td>
                            <td className="text-center">
                              <Badge variant="neutral">{verifier.verifier_type}</Badge>
                            </td>
                            <td className="text-center">
                              <Badge variant="info">{verifier.verification_count}</Badge>
                            </td>
                            <td className="text-center">
                              <Badge variant={verifier.status === 'active' ? 'success' : 'neutral'}>
                                {verifier.status}
                              </Badge>
                            </td>
                            <td className="text-center">
                              <Button 
                                size="sm" 
                                variant="danger"
                                onClick={() => deleteVerifier(verifier.id)}
                              >
                                Delete
                              </Button>
                            </td>
                          </tr>
                        ))}
                      </tbody>
                    </table>
                  </div>
                </InfoCard>
              </div>
            )}

            {/* MODULE 6: Monitor Verifications */}
            {activeModule === 'verifications' && !loading && (
              <div className="space-y-6">
                <div>
                  <h2 className="text-2xl font-bold text-secondary-800">Monitor Verifications</h2>
                  <p className="text-secondary-600 text-sm mt-1">Track all verification activities across the system</p>
                </div>
                
                <InfoCard>
                  <div className="table-container">
                    <table>
                      <thead>
                        <tr>
                          <th>Verification ID</th>
                          <th>Verifier</th>
                          <th className="text-center">Result</th>
                          <th className="text-center">Status</th>
                          <th className="text-center">Confidence</th>
                          <th className="text-center">Suspicious</th>
                          <th className="text-center">Actions</th>
                        </tr>
                      </thead>
                      <tbody>
                        {verifications.map(verif => (
                          <tr key={verif.id}>
                            <td className="font-mono text-xs">{verif.id.slice(0, 12)}...</td>
                            <td>{verif.verifier_id}</td>
                            <td className="text-center">
                              <Badge variant={verif.result ? 'success' : 'danger'}>
                                {verif.result ? 'Valid' : 'Invalid'}
                              </Badge>
                            </td>
                            <td className="text-center">
                              <Badge variant="info">{verif.status}</Badge>
                            </td>
                            <td className="text-center">
                              <span className="font-semibold">
                                {verif.confidence_score ? `${(verif.confidence_score * 100).toFixed(1)}%` : 'N/A'}
                              </span>
                            </td>
                            <td className="text-center">
                              {verif.is_suspicious ? (
                                <Badge variant="warning">
                                  <i className="fas fa-exclamation-triangle mr-1"></i> Yes
                                </Badge>
                              ) : (
                                <Badge variant="success">No</Badge>
                              )}
                            </td>
                            <td className="text-center">
                              {!verif.is_suspicious && (
                                <Button 
                                  size="sm" 
                                  variant="warning"
                                  onClick={() => flagVerification(verif.id)}
                                >
                                  Flag
                                </Button>
                              )}
                            </td>
                          </tr>
                        ))}
                      </tbody>
                    </table>
                  </div>
                </InfoCard>
              </div>
            )}

            {/* MODULE 7: Generate Reports */}
            {activeModule === 'reports' && !loading && (
              <div className="space-y-6">
                <div>
                  <h2 className="text-2xl font-bold text-secondary-800">AI-Powered Reports</h2>
                  <p className="text-secondary-600 mt-1">Generate comprehensive reports with AI insights and visual analytics</p>
                </div>
                
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
                  <InfoCard title="Institute Report" className="border-t-4 border-t-blue-500">
                    <div className="flex flex-col h-full justify-between">
                      <div>
                        <div className="w-12 h-12 rounded-lg bg-blue-100 flex items-center justify-center mb-4">
                          <i className="fas fa-building-columns text-blue-600 text-xl"></i>
                        </div>
                        <p className="text-sm text-secondary-600 mb-4">AI-powered analysis of institute performance with student and certificate metrics</p>
                      </div>
                      <Button 
                        onClick={() => generateReport('institute')}
                        variant="primary"
                        icon="fa-file-waveform"
                        className="w-full"
                      >
                        Generate Report
                      </Button>
                    </div>
                  </InfoCard>
                  
                  <InfoCard title="Certificate Report" className="border-t-4 border-t-green-500">
                    <div className="flex flex-col h-full justify-between">
                      <div>
                        <div className="w-12 h-12 rounded-lg bg-green-100 flex items-center justify-center mb-4">
                          <i className="fas fa-certificate text-green-600 text-xl"></i>
                        </div>
                        <p className="text-sm text-secondary-600 mb-4">Detailed certificate analytics with AI insights on issuance patterns and status</p>
                      </div>
                      <Button 
                        onClick={() => generateReport('certificates')}
                        variant="success"
                        icon="fa-file-waveform"
                        className="w-full"
                      >
                        Generate Report
                      </Button>
                    </div>
                  </InfoCard>
                  
                  <InfoCard title="Verification Report" className="border-t-4 border-t-purple-500">
                    <div className="flex flex-col h-full justify-between">
                      <div>
                        <div className="w-12 h-12 rounded-lg bg-purple-100 flex items-center justify-center mb-4">
                          <i className="fas fa-check-double text-purple-600 text-xl"></i>
                        </div>
                        <p className="text-sm text-secondary-600 mb-4">AI analysis of verification success rates and security patterns</p>
                      </div>
                      <Button 
                        onClick={() => generateReport('verifications')}
                        variant="primary"
                        icon="fa-file-waveform"
                        className="w-full"
                      >
                        Generate Report
                      </Button>
                    </div>
                  </InfoCard>
                  
                  <InfoCard title="System Activity Report" className="border-t-4 border-t-orange-500">
                    <div className="flex flex-col h-full justify-between">
                      <div>
                        <div className="w-12 h-12 rounded-lg bg-orange-100 flex items-center justify-center mb-4">
                          <i className="fas fa-chart-line text-orange-600 text-xl"></i>
                        </div>
                        <p className="text-sm text-secondary-600 mb-4">Complete system overview with AI-powered performance insights</p>
                      </div>
                      <Button 
                        onClick={() => generateReport('system')}
                        variant="warning"
                        icon="fa-file-waveform"
                        className="w-full"
                      >
                        Generate Report
                      </Button>
                    </div>
                  </InfoCard>
                </div>
                
                <InfoCard title="AI Features" icon="fa-robot">
                  <ul className="grid grid-cols-1 md:grid-cols-2 gap-3 text-sm text-secondary-700">
                    <li className="flex items-start gap-2">
                      <i className="fas fa-check-circle text-green-500 mt-0.5"></i>
                      <span>Executive summaries with key insights</span>
                    </li>
                    <li className="flex items-start gap-2">
                      <i className="fas fa-check-circle text-green-500 mt-0.5"></i>
                      <span>System health analysis and risk indicators</span>
                    </li>
                    <li className="flex items-start gap-2">
                      <i className="fas fa-check-circle text-green-500 mt-0.5"></i>
                      <span>Professional charts and visualizations</span>
                    </li>
                    <li className="flex items-start gap-2">
                      <i className="fas fa-check-circle text-green-500 mt-0.5"></i>
                      <span>Downloadable reports and images</span>
                    </li>
                  </ul>
                </InfoCard>
              </div>
            )}

            {/* MODULE 8: Feedback Management */}
            {activeModule === 'feedback' && !loading && (
              <div className="space-y-6">
                <div>
                  <h2 className="text-2xl font-bold text-secondary-800">Feedback Management</h2>
                  <p className="text-secondary-600 text-sm mt-1">Review and manage feedback from verifiers</p>
                </div>
                
                <InfoCard>
                  <div className="table-container">
                    <table>
                      <thead>
                        <tr>
                          <th>Feedback ID</th>
                          <th>Verifier</th>
                          <th>Message</th>
                          <th className="text-center">Category</th>
                          <th className="text-center">Priority</th>
                          <th className="text-center">Status</th>
                          <th className="text-center">Actions</th>
                        </tr>
                      </thead>
                      <tbody>
                        {feedbacks.map(fb => (
                          <tr key={fb.id}>
                            <td className="font-mono text-xs">{fb.id.slice(0, 12)}...</td>
                            <td>{fb.verifier_id}</td>
                            <td>
                              <span className="text-sm" title={fb.message}>
                                {fb.message.length > 50 ? fb.message.substring(0, 50) + '...' : fb.message}
                              </span>
                            </td>
                            <td className="text-center">
                              <Badge variant="neutral">{fb.category}</Badge>
                            </td>
                            <td className="text-center">
                              <Badge variant={fb.priority === 'high' ? 'danger' : fb.priority === 'medium' ? 'warning' : 'success'}>
                                {fb.priority}
                              </Badge>
                            </td>
                            <td className="text-center">
                              <Badge variant={fb.status === 'resolved' ? 'success' : 'info'}>
                                {fb.status}
                              </Badge>
                            </td>
                            <td className="text-center">
                              {!fb.flagged ? (
                                <Button 
                                  size="sm" 
                                  variant="warning"
                                  onClick={() => flagFeedback(fb.id)}
                                >
                                  Flag
                                </Button>
                              ) : (
                                <Badge variant="warning">
                                  <i className="fas fa-flag mr-1"></i> Flagged
                                </Badge>
                              )}
                            </td>
                          </tr>
                        ))}
                      </tbody>
                    </table>
                  </div>
                </InfoCard>
              </div>
            )}
        </div>
      </Layout>

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

      {/* AI Assistant Widget */}
      <AIAssistantWidget
        role="Admin"
        apiEndpoint="/admin/ai-query"
      />
    </>
  );
};

export default AdminDashboard;
