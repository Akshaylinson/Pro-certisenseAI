import React, { useState, useEffect } from 'react';
import { useAuth } from '../contexts/AuthContext';
import API_URL from '../config/api';

const InstituteDashboard = () => {
  const { user, token, logout } = useAuth();
  const [activeTab, setActiveTab] = useState('dashboard');
  const [students, setStudents] = useState([]);
  const [dashboard, setDashboard] = useState(null);
  const [loading, setLoading] = useState(false);
  const [newStudent, setNewStudent] = useState({ student_id: '', name: '', email: '', password: '' });
  const [certificateFile, setCertificateFile] = useState(null);
  const [selectedStudent, setSelectedStudent] = useState('');

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
    return response.json();
  };

  useEffect(() => {
    loadDashboard();
    loadStudents();
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

  const handleAddStudent = async (e) => {
    e.preventDefault();
    try {
      const response = await fetch(`${API_URL}/institute/students`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(newStudent)
      });

      if (response.ok) {
        setNewStudent({ student_id: '', name: '', email: '', password: '' });
        loadStudents();
        loadDashboard();
        alert('Student added successfully');
      }
    } catch (error) {
      alert('Error adding student');
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
    formData.append('student_id', selectedStudent);

    try {
      const response = await fetch(`${API_URL}/institute/certificates`, {
        method: 'POST',
        headers: { 'Authorization': `Bearer ${token}` },
        body: formData
      });

      if (response.ok) {
        setCertificateFile(null);
        setSelectedStudent('');
        loadDashboard();
        alert('Certificate issued successfully');
      }
    } catch (error) {
      alert('Error issuing certificate');
    }
  };

  const renderDashboard = () => (
    <div className="space-y-6">
      <h3 className="text-lg font-semibold">School Dashboard</h3>
      
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div className="bg-blue-50 p-4 rounded-lg">
          <h4 className="font-medium text-blue-900">Total Students</h4>
          <p className="text-3xl font-bold text-blue-600">{dashboard?.total_students || 0}</p>
        </div>
        <div className="bg-green-50 p-4 rounded-lg">
          <h4 className="font-medium text-green-900">Certificates Issued</h4>
          <p className="text-3xl font-bold text-green-600">{dashboard?.total_certificates || 0}</p>
        </div>
        <div className="bg-purple-50 p-4 rounded-lg">
          <h4 className="font-medium text-purple-900">Verifications</h4>
          <p className="text-3xl font-bold text-purple-600">{dashboard?.total_verifications || 0}</p>
        </div>
      </div>
    </div>
  );

  const renderStudents = () => (
    <div className="space-y-6">
      <h3 className="text-lg font-semibold">Manage Students</h3>
      
      <form onSubmit={handleAddStudent} className="bg-gray-50 p-4 rounded-lg space-y-3">
        <h4 className="font-medium">Add New Student</h4>
        <input
          type="text"
          value={newStudent.student_id}
          onChange={(e) => setNewStudent({ ...newStudent, student_id: e.target.value })}
          placeholder="Student ID"
          className="w-full px-3 py-2 border rounded-md"
          required
        />
        <input
          type="text"
          value={newStudent.name}
          onChange={(e) => setNewStudent({ ...newStudent, name: e.target.value })}
          placeholder="Full Name"
          className="w-full px-3 py-2 border rounded-md"
          required
        />
        <input
          type="email"
          value={newStudent.email}
          onChange={(e) => setNewStudent({ ...newStudent, email: e.target.value })}
          placeholder="Email"
          className="w-full px-3 py-2 border rounded-md"
          required
        />
        <input
          type="password"
          value={newStudent.password}
          onChange={(e) => setNewStudent({ ...newStudent, password: e.target.value })}
          placeholder="Password"
          className="w-full px-3 py-2 border rounded-md"
          required
        />
        <button type="submit" className="w-full px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700">
          Add Student
        </button>
      </form>

      <div className="space-y-3">
        <h4 className="font-medium">Students List</h4>
        {loading ? (
          <div className="text-center py-8">Loading...</div>
        ) : students.length === 0 ? (
          <div className="text-center py-8 text-gray-600">No students added yet</div>
        ) : (
          <div className="space-y-2">
            {students.map(student => (
              <div key={student.id} className="border p-3 rounded-lg">
                <p className="font-medium">{student.name}</p>
                <p className="text-sm text-gray-600">ID: {student.student_id}</p>
                <p className="text-sm text-gray-600">Email: {student.email}</p>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );

  const renderCertificates = () => (
    <div className="space-y-6">
      <h3 className="text-lg font-semibold">Issue Certificates</h3>
      
      <form onSubmit={handleIssueCertificate} className="bg-gray-50 p-4 rounded-lg space-y-3">
        <div>
          <label className="block text-sm font-medium mb-2">Select Student</label>
          <select
            value={selectedStudent}
            onChange={(e) => setSelectedStudent(e.target.value)}
            className="w-full px-3 py-2 border rounded-md"
            required
          >
            <option value="">Choose a student...</option>
            {students.map(student => (
              <option key={student.id} value={student.student_id}>
                {student.name} ({student.student_id})
              </option>
            ))}
          </select>
        </div>

        <div>
          <label className="block text-sm font-medium mb-2">Certificate File</label>
          <input
            type="file"
            accept=".pdf,.jpg,.png"
            onChange={(e) => setCertificateFile(e.target.files[0])}
            className="w-full px-3 py-2 border rounded-md"
            required
          />
        </div>

        <button type="submit" className="w-full px-4 py-2 bg-green-600 text-white rounded hover:bg-green-700">
          Issue Certificate
        </button>
      </form>
    </div>
  );

  return (
    <div className="min-h-screen bg-gray-50">
      <nav className="bg-white shadow-sm border-b">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between h-16">
            <div className="flex items-center">
              <h1 className="text-xl font-semibold">Institute Dashboard</h1>
            </div>
            <div className="flex items-center space-x-4">
              <span className="text-sm text-gray-600">Institute Admin</span>
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
                { key: 'dashboard', label: 'Dashboard' },
                { key: 'students', label: 'Manage Students' },
                { key: 'certificates', label: 'Issue Certificates' }
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
              {activeTab === 'dashboard' && renderDashboard()}
              {activeTab === 'students' && renderStudents()}
              {activeTab === 'certificates' && renderCertificates()}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default InstituteDashboard;