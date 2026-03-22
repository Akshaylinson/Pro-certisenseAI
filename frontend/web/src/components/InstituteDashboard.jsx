import { useState, useEffect } from 'react';
import { useAuth } from '../contexts/AuthContext';
import axios from 'axios';
import Layout from './Layout';
import { StatCard, InfoCard, Button, Badge } from './UIComponents';
import API_URL from '../config/api';

const InstituteDashboard = () => {
  const { token, logout } = useAuth();
  const [activeTab, setActiveTab] = useState('dashboard');
  const [students, setStudents] = useState([]);
  const [dashboard, setDashboard] = useState(null);
  const [profile, setProfile] = useState(null);
  const [loading, setLoading] = useState(false);
  const [newStudent, setNewStudent] = useState({ name: '', email: '', password: '' });
  const [showAddStudent, setShowAddStudent] = useState(false);
  const [certificateFile, setCertificateFile] = useState(null);
  const [selectedStudent, setSelectedStudent] = useState('');
  const [profileImage, setProfileImage] = useState(null);
  const [editingProfile, setEditingProfile] = useState(false);
  const [editingStudent, setEditingStudent] = useState(null);
  const [editStudentData, setEditStudentData] = useState({});
  const [chatMessages, setChatMessages] = useState([
    { role: 'bot', content: 'Hello! I\'m your institute assistant. Ask me about students, certificates, or recent activity.' }
  ]);
  const [chatInput, setChatInput] = useState('');

  const headers = { Authorization: `Bearer ${token}` };

  const apiCall = async (endpoint, method = 'GET', body = null) => {
    const options = {
      method,
      headers: {
        'Authorization': `Bearer ${token}`,
        ...(body && { 'Content-Type': 'application/json' })
      },
      ...(body && { body: JSON.stringify(body) })
    };
    const response = await fetch(`${API_URL}${endpoint}`, options);
    if (!response.ok) {
      const errorText = await response.text();
      throw new Error(`API Error: ${response.status} - ${errorText}`);
    }
    return response.json();
  };

  const navigationItems = [
    { id: 'dashboard', label: 'Dashboard' },
    { id: 'students', label: 'Students' },
    { id: 'certificates', label: 'Certificates' },
    { id: 'profile', label: 'Profile' },
    { id: 'chatbot', label: 'AI Assistant' },
  ];

  useEffect(() => {
    loadDashboard();
    loadStudents();
    loadProfile();
  }, []);

  const loadDashboard = async () => {
    try {
      const data = await apiCall('/institute/dashboard');
      setDashboard(data);
    } catch (error) {
      console.error('Error loading dashboard:', error);
    }
  };

  const loadStudents = async () => {
    setLoading(true);
    try {
      const data = await apiCall('/institute/students');
      setStudents(data.students || []);
    } catch (error) {
      console.error('Error loading students:', error);
    } finally {
      setLoading(false);
    }
  };

  const loadProfile = async () => {
    try {
      const data = await apiCall('/institute/profile');
      setProfile(data);
    } catch (error) {
      console.error('Error loading profile:', error);
    }
  };

  const handleAddStudent = async (e) => {
    e.preventDefault();
    try {
      const formData = new FormData();
      formData.append('name', newStudent.name);
      formData.append('email', newStudent.email);
      formData.append('password', newStudent.password);
      const response = await fetch(`${API_URL}/institute/students`, {
        method: 'POST',
        headers: { 'Authorization': `Bearer ${token}` },
        body: formData
      });
      const result = await response.json();
      if (response.ok) {
        setNewStudent({ name: '', email: '', password: '' });
        setShowAddStudent(false);
        loadStudents();
        loadDashboard();
        alert(`Student added! Student ID: ${result.student_id}`);
      } else {
        alert(result.detail || 'Error adding student');
      }
    } catch (error) {
      alert('Error adding student');
    }
  };

  const handleEditStudent = async (studentId) => {
    try {
      const response = await fetch(
        `${API_URL}/institute/students/${studentId}?name=${encodeURIComponent(editStudentData.name)}&email=${encodeURIComponent(editStudentData.email)}`,
        { method: 'PUT', headers: { 'Authorization': `Bearer ${token}` } }
      );
      if (response.ok) {
        loadStudents();
        setEditingStudent(null);
        setEditStudentData({});
      } else {
        alert('Error updating student');
      }
    } catch {
      alert('Error updating student');
    }
  };

  const handleIssueCertificate = async (e) => {
    e.preventDefault();
    if (!certificateFile || !selectedStudent) {
      alert('Please select a student and certificate file');
      return;
    }
    const formData = new FormData();
    formData.append('file', certificateFile);
    try {
      const response = await fetch(
        `${API_URL}/institute/certificates?student_id=${encodeURIComponent(selectedStudent)}`,
        { method: 'POST', headers: { 'Authorization': `Bearer ${token}` }, body: formData }
      );
      if (response.ok) {
        const result = await response.json();
        setCertificateFile(null);
        setSelectedStudent('');
        loadDashboard();
        alert(`Certificate issued!\nID: ${result.certificate_id}\nHash: ${result.hash.substring(0, 16)}...`);
      } else {
        const errorData = await response.json().catch(() => ({ detail: 'Unknown error' }));
        alert(`Error: ${errorData.detail || 'Unknown error'}`);
      }
    } catch (error) {
      alert(`Error: ${error.message}`);
    }
  };

  const sendChatMessage = async () => {
    if (!chatInput.trim()) return;
    const userMessage = { role: 'user', content: chatInput };
    setChatMessages(prev => [...prev, userMessage]);
    setChatInput('');
    try {
      const res = await axios.get(`${API_URL}/institute/ai-query`, {
        params: { query: chatInput },
        headers: { 'Authorization': `Bearer ${token}` }
      });
      setChatMessages(prev => [...prev, { role: 'bot', content: res.data.response }]);
    } catch {
      setChatMessages(prev => [...prev, { role: 'bot', content: 'Sorry, I encountered an error. Please try again.' }]);
    }
  };

  const handleUpdateProfile = async (e) => {
    e.preventDefault();
    const formData = new FormData();
    formData.append('institute_name', profile.institute_name);
    formData.append('institute_id', profile.institute_id);
    formData.append('email', profile.email);
    formData.append('location', profile.location || '');
    formData.append('description', profile.description || '');
    if (profileImage) formData.append('image', profileImage);
    try {
      const response = await fetch(`${API_URL}/institute/profile`, {
        method: 'PUT',
        headers: { 'Authorization': `Bearer ${token}` },
        body: formData
      });
      if (response.ok) {
        loadProfile();
        setEditingProfile(false);
        setProfileImage(null);
        alert('Profile updated successfully');
      }
    } catch {
      alert('Error updating profile');
    }
  };

  // ─── RENDER: DASHBOARD ───────────────────────────────────────────────────────
  const renderDashboard = () => (
    <div className="space-y-6">
      <div className="mb-6">
        <h2 className="text-2xl font-bold text-secondary-800 mb-1">Institute Overview</h2>
        <p className="text-secondary-600">Summary of your students, certificates and verifications</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <StatCard
          title="Total Students"
          value={dashboard?.total_students ?? 0}
          icon="fa-user-graduate"
          color="blue"
        />
        <StatCard
          title="Certificates Issued"
          value={dashboard?.total_certificates ?? 0}
          icon="fa-certificate"
          color="green"
        />
        <StatCard
          title="Total Verifications"
          value={dashboard?.total_verifications ?? 0}
          icon="fa-check-double"
          color="purple"
        />
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <InfoCard title="Quick Actions">
          <div className="space-y-3">
            <Button icon="fa-user-plus" onClick={() => { setActiveTab('students'); setShowAddStudent(true); }} className="w-full justify-center">
              Add New Student
            </Button>
            <Button icon="fa-file-certificate" variant="success" onClick={() => setActiveTab('certificates')} className="w-full justify-center">
              Issue Certificate
            </Button>
            <Button icon="fa-robot" variant="secondary" onClick={() => setActiveTab('chatbot')} className="w-full justify-center">
              Ask AI Assistant
            </Button>
          </div>
        </InfoCard>

        <InfoCard title="Institute Info">
          <div className="space-y-3">
            <div className="flex items-center gap-3 p-3 bg-secondary-50 rounded-lg">
              <div className="w-10 h-10 rounded-full bg-purple-100 flex items-center justify-center">
                <i className="fas fa-building-columns text-purple-600"></i>
              </div>
              <div>
                <p className="text-xs text-secondary-500">Institute Name</p>
                <p className="font-semibold text-secondary-800">{profile?.institute_name || '—'}</p>
              </div>
            </div>
            <div className="flex items-center gap-3 p-3 bg-secondary-50 rounded-lg">
              <div className="w-10 h-10 rounded-full bg-blue-100 flex items-center justify-center">
                <i className="fas fa-id-badge text-blue-600"></i>
              </div>
              <div>
                <p className="text-xs text-secondary-500">Institute ID</p>
                <p className="font-mono font-semibold text-secondary-800">{profile?.institute_id || '—'}</p>
              </div>
            </div>
            <div className="flex items-center gap-3 p-3 bg-secondary-50 rounded-lg">
              <div className="w-10 h-10 rounded-full bg-green-100 flex items-center justify-center">
                <i className="fas fa-location-dot text-green-600"></i>
              </div>
              <div>
                <p className="text-xs text-secondary-500">Location</p>
                <p className="font-semibold text-secondary-800">{profile?.location || 'Not specified'}</p>
              </div>
            </div>
          </div>
        </InfoCard>
      </div>
    </div>
  );

  // ─── RENDER: STUDENTS ────────────────────────────────────────────────────────
  const renderStudents = () => (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <div>
          <h2 className="text-2xl font-bold text-secondary-800">Manage Students</h2>
          <p className="text-secondary-600 text-sm mt-1">Add and manage students in your institute</p>
        </div>
        <Button icon="fa-user-plus" onClick={() => setShowAddStudent(!showAddStudent)}>
          Add Student
        </Button>
      </div>

      {showAddStudent && (
        <InfoCard title="Add New Student">
          <div className="mb-3 p-3 bg-blue-50 border border-blue-200 rounded-lg text-sm text-blue-800">
            <i className="fas fa-info-circle mr-2"></i>
            Student ID auto-generated as <span className="font-mono font-semibold">[{profile?.institute_id || 'INST'}-00001]</span>
          </div>
          <form onSubmit={handleAddStudent} className="space-y-4">
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              <div>
                <label className="block font-medium mb-1">Full Name *</label>
                <input
                  type="text"
                  value={newStudent.name}
                  onChange={(e) => setNewStudent({ ...newStudent, name: e.target.value })}
                  className="w-full"
                  placeholder="e.g. John Doe"
                  required
                />
              </div>
              <div>
                <label className="block font-medium mb-1">Email *</label>
                <input
                  type="email"
                  value={newStudent.email}
                  onChange={(e) => setNewStudent({ ...newStudent, email: e.target.value })}
                  className="w-full"
                  placeholder="student@email.com"
                  required
                />
              </div>
              <div>
                <label className="block font-medium mb-1">Password *</label>
                <input
                  type="password"
                  value={newStudent.password}
                  onChange={(e) => setNewStudent({ ...newStudent, password: e.target.value })}
                  className="w-full"
                  placeholder="Min 6 characters"
                  required
                />
              </div>
            </div>
            <div className="flex gap-2 pt-2">
              <Button type="submit" variant="success" icon="fa-check">Create Student</Button>
              <Button type="button" variant="secondary" onClick={() => setShowAddStudent(false)}>Cancel</Button>
            </div>
          </form>
        </InfoCard>
      )}

      <InfoCard title={`Students (${students.length})`}>
        {loading ? (
          <div className="text-center py-12">
            <div className="loading-spinner mx-auto mb-4"></div>
            <p className="text-secondary-600">Loading students...</p>
          </div>
        ) : students.length === 0 ? (
          <div className="text-center py-12 text-secondary-500">
            <i className="fas fa-users text-4xl mb-3 block opacity-30"></i>
            No students added yet
          </div>
        ) : (
          <div className="table-container">
            <table>
              <thead>
                <tr>
                  <th>Student ID</th>
                  <th>Name</th>
                  <th>Email</th>
                  <th className="text-center">Actions</th>
                </tr>
              </thead>
              <tbody>
                {students.map(student => (
                  <tr key={student.id}>
                    {editingStudent === student.id ? (
                      <>
                        <td><span className="font-mono text-xs">{student.student_id}</span></td>
                        <td>
                          <input
                            type="text"
                            value={editStudentData.name}
                            onChange={(e) => setEditStudentData({ ...editStudentData, name: e.target.value })}
                            className="w-full px-2 py-1 border rounded text-sm"
                          />
                        </td>
                        <td>
                          <input
                            type="email"
                            value={editStudentData.email}
                            onChange={(e) => setEditStudentData({ ...editStudentData, email: e.target.value })}
                            className="w-full px-2 py-1 border rounded text-sm"
                          />
                        </td>
                        <td className="text-center">
                          <div className="flex gap-2 justify-center">
                            <Button size="sm" variant="success" icon="fa-check" onClick={() => handleEditStudent(student.id)}>Save</Button>
                            <Button size="sm" variant="secondary" onClick={() => setEditingStudent(null)}>Cancel</Button>
                          </div>
                        </td>
                      </>
                    ) : (
                      <>
                        <td><span className="font-mono text-xs bg-secondary-100 px-2 py-1 rounded">{student.student_id}</span></td>
                        <td className="font-semibold">{student.name}</td>
                        <td className="text-secondary-600">{student.email}</td>
                        <td className="text-center">
                          <Button
                            size="sm"
                            icon="fa-pen"
                            onClick={() => { setEditingStudent(student.id); setEditStudentData({ name: student.name, email: student.email }); }}
                          >
                            Edit
                          </Button>
                        </td>
                      </>
                    )}
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </InfoCard>
    </div>
  );

  // ─── RENDER: CERTIFICATES ────────────────────────────────────────────────────
  const renderCertificates = () => (
    <div className="space-y-6">
      <div>
        <h2 className="text-2xl font-bold text-secondary-800">Issue Certificates</h2>
        <p className="text-secondary-600 text-sm mt-1">Upload and issue certificates to your students on the blockchain</p>
      </div>

      <InfoCard title="Issue New Certificate">
        <form onSubmit={handleIssueCertificate} className="space-y-4">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label className="block font-medium mb-2">Select Student *</label>
              <select
                value={selectedStudent}
                onChange={(e) => setSelectedStudent(e.target.value)}
                className="w-full px-3 py-2 border border-secondary-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500"
                required
              >
                <option value="">Choose a student...</option>
                {students.map(student => (
                  <option key={student.id} value={student.student_id}>
                    {student.name} — {student.student_id}
                  </option>
                ))}
              </select>
            </div>
            <div>
              <label className="block font-medium mb-2">Certificate File *</label>
              <input
                type="file"
                accept=".pdf,.jpg,.png"
                onChange={(e) => setCertificateFile(e.target.files[0])}
                className="w-full px-3 py-2 border border-secondary-200 rounded-lg text-sm"
                required
              />
              <p className="text-xs text-secondary-500 mt-1">Supported: PDF, JPG, PNG</p>
            </div>
          </div>

          {selectedStudent && certificateFile && (
            <div className="p-3 bg-green-50 border border-green-200 rounded-lg text-sm text-green-800">
              <i className="fas fa-check-circle mr-2"></i>
              Ready to issue certificate for <strong>{students.find(s => s.student_id === selectedStudent)?.name}</strong> — file: <strong>{certificateFile.name}</strong>
            </div>
          )}

          <Button type="submit" variant="success" icon="fa-file-certificate">
            Issue Certificate on Blockchain
          </Button>
        </form>
      </InfoCard>

      <InfoCard title="How It Works">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          {[
            { step: '1', icon: 'fa-upload', title: 'Upload', desc: 'Select the student and upload the certificate file', color: 'blue' },
            { step: '2', icon: 'fa-link', title: 'Blockchain', desc: 'Certificate hash is stored immutably on the blockchain', color: 'purple' },
            { step: '3', icon: 'fa-shield-check', title: 'Verify', desc: 'Anyone can verify the certificate using its ID or hash', color: 'green' },
          ].map(({ step, icon, title, desc, color }) => (
            <div key={step} className={`p-4 bg-${color}-50 rounded-lg text-center`}>
              <div className={`w-10 h-10 rounded-full bg-${color}-100 flex items-center justify-center mx-auto mb-2`}>
                <i className={`fas ${icon} text-${color}-600`}></i>
              </div>
              <p className="font-semibold text-secondary-800">{title}</p>
              <p className="text-xs text-secondary-600 mt-1">{desc}</p>
            </div>
          ))}
        </div>
      </InfoCard>
    </div>
  );

  // ─── RENDER: PROFILE ─────────────────────────────────────────────────────────
  const renderProfile = () => (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <div>
          <h2 className="text-2xl font-bold text-secondary-800">Institute Profile</h2>
          <p className="text-secondary-600 text-sm mt-1">View and manage your institute information</p>
        </div>
        <Button
          icon={editingProfile ? 'fa-times' : 'fa-pen'}
          variant={editingProfile ? 'secondary' : 'primary'}
          onClick={() => setEditingProfile(!editingProfile)}
        >
          {editingProfile ? 'Cancel' : 'Edit Profile'}
        </Button>
      </div>

      {profile && (
        <InfoCard>
          {!editingProfile ? (
            <div className="space-y-6">
              <div className="flex items-center gap-5">
                <div className="w-20 h-20 bg-purple-100 rounded-full flex items-center justify-center shrink-0">
                  {profile.image ? (
                    <img src={profile.image} alt="Institute" className="w-20 h-20 rounded-full object-cover" />
                  ) : (
                    <span className="text-3xl font-bold text-purple-600">{profile.institute_name?.charAt(0)}</span>
                  )}
                </div>
                <div>
                  <h3 className="text-xl font-bold text-secondary-800">{profile.institute_name}</h3>
                  <span className="font-mono text-sm bg-secondary-100 px-2 py-1 rounded text-secondary-600">{profile.institute_id}</span>
                  <Badge variant="success" className="ml-2">Approved</Badge>
                </div>
              </div>

              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                {[
                  { label: 'Email', value: profile.email, icon: 'fa-envelope' },
                  { label: 'Location', value: profile.location || 'Not specified', icon: 'fa-location-dot' },
                ].map(({ label, value, icon }) => (
                  <div key={label} className="p-4 bg-secondary-50 rounded-lg">
                    <div className="flex items-center gap-2 mb-1">
                      <i className={`fas ${icon} text-secondary-400 text-sm`}></i>
                      <p className="text-xs font-medium text-secondary-500 uppercase tracking-wide">{label}</p>
                    </div>
                    <p className="text-secondary-800 font-medium">{value}</p>
                  </div>
                ))}
              </div>

              <div className="p-4 bg-secondary-50 rounded-lg">
                <div className="flex items-center gap-2 mb-1">
                  <i className="fas fa-align-left text-secondary-400 text-sm"></i>
                  <p className="text-xs font-medium text-secondary-500 uppercase tracking-wide">Description</p>
                </div>
                <p className="text-secondary-800">{profile.description || 'No description provided'}</p>
              </div>
            </div>
          ) : (
            <form onSubmit={handleUpdateProfile} className="space-y-4">
              <div className="flex items-center gap-4">
                <div className="w-20 h-20 bg-purple-100 rounded-full flex items-center justify-center shrink-0">
                  {profileImage ? (
                    <img src={URL.createObjectURL(profileImage)} alt="Preview" className="w-20 h-20 rounded-full object-cover" />
                  ) : profile.image ? (
                    <img src={profile.image} alt="Institute" className="w-20 h-20 rounded-full object-cover" />
                  ) : (
                    <span className="text-3xl font-bold text-purple-600">{profile.institute_name?.charAt(0)}</span>
                  )}
                </div>
                <div>
                  <label className="block text-sm font-medium text-secondary-700 mb-1">Profile Image</label>
                  <input type="file" accept="image/*" onChange={(e) => setProfileImage(e.target.files[0])} className="text-sm" />
                </div>
              </div>

              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                  <label className="block font-medium mb-1">Institute Name *</label>
                  <input type="text" value={profile.institute_name} onChange={(e) => setProfile({ ...profile, institute_name: e.target.value })} className="w-full" required />
                </div>
                <div>
                  <label className="block font-medium mb-1">Institute ID *</label>
                  <input type="text" value={profile.institute_id} onChange={(e) => setProfile({ ...profile, institute_id: e.target.value })} className="w-full font-mono" required />
                  <p className="text-xs text-secondary-500 mt-1">Used for student IDs: {profile.institute_id}-00001</p>
                </div>
                <div>
                  <label className="block font-medium mb-1">Email *</label>
                  <input type="email" value={profile.email} onChange={(e) => setProfile({ ...profile, email: e.target.value })} className="w-full" required />
                </div>
                <div>
                  <label className="block font-medium mb-1">Location</label>
                  <input type="text" value={profile.location || ''} onChange={(e) => setProfile({ ...profile, location: e.target.value })} className="w-full" placeholder="City, Country" />
                </div>
              </div>
              <div>
                <label className="block font-medium mb-1">Description</label>
                <textarea value={profile.description || ''} onChange={(e) => setProfile({ ...profile, description: e.target.value })} rows={3} className="w-full px-3 py-2 border border-secondary-200 rounded-lg" placeholder="Brief description about your institute..." />
              </div>
              <div className="flex gap-2 pt-2">
                <Button type="submit" variant="success" icon="fa-check">Save Changes</Button>
                <Button type="button" variant="secondary" onClick={() => setEditingProfile(false)}>Cancel</Button>
              </div>
            </form>
          )}
        </InfoCard>
      )}
    </div>
  );

  // ─── RENDER: CHATBOT ─────────────────────────────────────────────────────────
  const renderChatbot = () => (
    <div className="space-y-6">
      <div>
        <h2 className="text-2xl font-bold text-secondary-800">AI Assistant</h2>
        <p className="text-secondary-600 text-sm mt-1">Ask about your students, certificates, and institute statistics</p>
      </div>

      <InfoCard>
        <div className="h-[420px] overflow-y-auto mb-4 space-y-3 pr-1">
          {chatMessages.map((msg, idx) => (
            <div key={idx} className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}>
              {msg.role === 'bot' && (
                <div className="w-8 h-8 rounded-full bg-purple-100 flex items-center justify-center mr-2 shrink-0 mt-1">
                  <i className="fas fa-robot text-purple-600 text-xs"></i>
                </div>
              )}
              <div className={`max-w-[78%] px-4 py-3 rounded-xl shadow-sm text-sm ${
                msg.role === 'user'
                  ? 'bg-purple-600 text-white rounded-br-none'
                  : 'bg-secondary-50 border border-secondary-200 text-secondary-800 rounded-bl-none'
              }`}>
                <pre className="whitespace-pre-wrap font-sans">{msg.content}</pre>
              </div>
            </div>
          ))}
        </div>

        <div className="flex gap-2">
          <input
            type="text"
            value={chatInput}
            onChange={(e) => setChatInput(e.target.value)}
            onKeyPress={(e) => e.key === 'Enter' && sendChatMessage()}
            className="flex-1 px-4 py-2 border border-secondary-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-purple-500"
            placeholder="Ask: 'How many students?' or 'Show statistics'"
          />
          <Button icon="fa-paper-plane" onClick={sendChatMessage}>Send</Button>
        </div>
      </InfoCard>

      <InfoCard title="Suggested Questions">
        <div className="grid grid-cols-2 md:grid-cols-4 gap-2">
          {['Show my statistics', 'How many students?', 'Certificate information', 'Recent activity'].map(q => (
            <button
              key={q}
              onClick={() => setChatInput(q)}
              className="text-left px-3 py-2 bg-purple-50 hover:bg-purple-100 text-purple-700 text-sm rounded-lg transition border border-purple-200"
            >
              <i className="fas fa-comment-dots mr-1"></i> {q}
            </button>
          ))}
        </div>
      </InfoCard>
    </div>
  );

  return (
    <Layout
      title="Institute Dashboard"
      subtitle="Certificate Management System"
      userRole={profile?.institute_name || 'Institute Admin'}
      onLogout={logout}
      navigationItems={navigationItems}
      activeTab={activeTab}
      onModuleChange={setActiveTab}
      themeColor="purple"
    >
      <div className="space-y-6">
        {activeTab === 'dashboard'    && renderDashboard()}
        {activeTab === 'students'     && renderStudents()}
        {activeTab === 'certificates' && renderCertificates()}
        {activeTab === 'profile'      && renderProfile()}
        {activeTab === 'chatbot'      && renderChatbot()}
      </div>
    </Layout>
  );
};

export default InstituteDashboard;
