import React, { useState, useEffect } from 'react';
import { useAuth } from '../contexts/AuthContext';

const InstituteDashboard = () => {
  const { user, token, logout } = useAuth();
  const [activeTab, setActiveTab] = useState('dashboard');
  const [students, setStudents] = useState([]);
  const [dashboard, setDashboard] = useState(null);
  const [profile, setProfile] = useState(null);
  const [loading, setLoading] = useState(false);
  const [newStudent, setNewStudent] = useState({ name: '', email: '', password: '' });
  const [certificateFile, setCertificateFile] = useState(null);
  const [selectedStudent, setSelectedStudent] = useState('');
  const [profileImage, setProfileImage] = useState(null);
  const [editingProfile, setEditingProfile] = useState(false);
  const [editingStudent, setEditingStudent] = useState(null);

  const apiCall = async (endpoint, method = 'GET', body = null) => {
    try {
      const options = {
        method,
        headers: {
          'Authorization': `Bearer ${token}`,
          ...(body && { 'Content-Type': 'application/json' })
        },
        ...(body && { body: JSON.stringify(body) })
      };

      console.log(`Making API call to: ${endpoint}`);
      console.log(`Headers:`, options.headers);
      
      const response = await fetch(`http://localhost:8000${endpoint}`, options);
      
      console.log(`Response status: ${response.status}`);
      
      if (!response.ok) {
        const errorText = await response.text();
        console.error(`API Error: ${response.status} - ${errorText}`);
        throw new Error(`API Error: ${response.status} - ${errorText}`);
      }
      
      const data = await response.json();
      console.log(`Response data:`, data);
      return data;
    } catch (error) {
      console.error(`API call failed for ${endpoint}:`, error);
      throw error;
    }
  };

  useEffect(() => {
    loadDashboard();
    loadStudents();
    loadProfile();
  }, []);

  const loadDashboard = async () => {
    try {
      console.log('Loading dashboard...');
      const data = await apiCall('/institute/dashboard');
      setDashboard(data);
      console.log('Dashboard loaded successfully:', data);
    } catch (error) {
      console.error('Error loading dashboard:', error);
      alert(`Failed to load dashboard: ${error.message}`);
    }
  };

  const loadStudents = async () => {
    setLoading(true);
    try {
      console.log('Loading students...');
      const data = await apiCall('/institute/students');
      setStudents(data.students || []);
      console.log('Students loaded successfully:', data.students?.length || 0);
    } catch (error) {
      console.error('Error loading students:', error);
      alert(`Failed to load students: ${error.message}`);
    } finally {
      setLoading(false);
    }
  };

  const loadProfile = async () => {
    try {
      console.log('Loading profile...');
      const data = await apiCall('/institute/profile');
      setProfile(data);
      console.log('Profile loaded successfully:', data);
    } catch (error) {
      console.error('Error loading profile:', error);
      alert(`Failed to load profile: ${error.message}`);
    }
  };

  const handleAddStudent = async (e) => {
    e.preventDefault();
    try {
      const response = await fetch(`http://localhost:8000/institute/students?name=${encodeURIComponent(newStudent.name)}&email=${encodeURIComponent(newStudent.email)}&password=${encodeURIComponent(newStudent.password)}`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });

      const result = await response.json();
      if (response.ok) {
        setNewStudent({ name: '', email: '', password: '' });
        loadStudents();
        loadDashboard();
        alert(`Student added successfully! Student ID: ${result.student_id}`);
      } else {
        alert(result.detail || 'Error adding student');
      }
    } catch (error) {
      alert('Error adding student');
    }
  };

  const handleEditStudent = async (studentId, updatedData) => {
    try {
      const response = await fetch(`http://localhost:8000/institute/students/${studentId}?name=${encodeURIComponent(updatedData.name)}&email=${encodeURIComponent(updatedData.email)}`, {
        method: 'PUT',
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });

      if (response.ok) {
        loadStudents();
        setEditingStudent(null);
        alert('Student updated successfully');
      } else {
        alert('Error updating student');
      }
    } catch (error) {
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
      const response = await fetch(`http://localhost:8000/institute/certificates?student_id=${encodeURIComponent(selectedStudent)}`, {
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

  const handleUpdateProfile = async (e) => {
    e.preventDefault();
    const formData = new FormData();
    formData.append('institute_name', profile.institute_name);
    formData.append('institute_id', profile.institute_id);
    formData.append('email', profile.email);
    formData.append('location', profile.location);
    formData.append('description', profile.description || '');
    if (profileImage) {
      formData.append('image', profileImage);
    }

    try {
      const response = await fetch('http://localhost:8000/institute/profile', {
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
    } catch (error) {
      alert('Error updating profile');
    }
  };

  const renderDashboard = () => (
    <div className="space-y-6">
      <h3 className="text-lg font-semibold">Institute Dashboard</h3>
      
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

  const renderProfile = () => (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <h3 className="text-lg font-semibold">Institute Profile</h3>
        <button
          onClick={() => setEditingProfile(!editingProfile)}
          className="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700"
        >
          {editingProfile ? 'Cancel' : 'Edit Profile'}
        </button>
      </div>

      {profile && (
        <div className="bg-white border rounded-lg p-6">
          {!editingProfile ? (
            <div className="space-y-4">
              <div className="flex items-center space-x-4">
                <div className="w-20 h-20 bg-gray-200 rounded-full flex items-center justify-center">
                  {profile.image ? (
                    <img src={profile.image} alt="Institute" className="w-20 h-20 rounded-full object-cover" />
                  ) : (
                    <span className="text-2xl font-bold text-gray-600">{profile.institute_name?.charAt(0)}</span>
                  )}
                </div>
                <div>
                  <h4 className="text-xl font-semibold">{profile.institute_name}</h4>
                  <p className="text-gray-600">Institute ID: <span className="font-mono bg-gray-100 px-2 py-1 rounded">{profile.institute_id}</span></p>
                </div>
              </div>
              
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700">Email</label>
                  <p className="mt-1 text-sm text-gray-900">{profile.email}</p>
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700">Location</label>
                  <p className="mt-1 text-sm text-gray-900">{profile.location || 'Not specified'}</p>
                </div>
              </div>
              
              <div>
                <label className="block text-sm font-medium text-gray-700">Description</label>
                <p className="mt-1 text-sm text-gray-900">{profile.description || 'No description provided'}</p>
              </div>
            </div>
          ) : (
            <form onSubmit={handleUpdateProfile} className="space-y-4">
              <div className="flex items-center space-x-4">
                <div className="w-20 h-20 bg-gray-200 rounded-full flex items-center justify-center">
                  {profileImage ? (
                    <img src={URL.createObjectURL(profileImage)} alt="Preview" className="w-20 h-20 rounded-full object-cover" />
                  ) : profile.image ? (
                    <img src={profile.image} alt="Institute" className="w-20 h-20 rounded-full object-cover" />
                  ) : (
                    <span className="text-2xl font-bold text-gray-600">{profile.institute_name?.charAt(0)}</span>
                  )}
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700">Profile Image</label>
                  <input
                    type="file"
                    accept="image/*"
                    onChange={(e) => setProfileImage(e.target.files[0])}
                    className="mt-1 text-sm"
                  />
                </div>
              </div>

              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700">Institute Name</label>
                  <input
                    type="text"
                    value={profile.institute_name}
                    onChange={(e) => setProfile({...profile, institute_name: e.target.value})}
                    className="mt-1 w-full px-3 py-2 border rounded-md"
                    required
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700">Institute ID</label>
                  <input
                    type="text"
                    value={profile.institute_id}
                    onChange={(e) => setProfile({...profile, institute_id: e.target.value})}
                    className="mt-1 w-full px-3 py-2 border rounded-md font-mono"
                    placeholder="e.g., MIT, HARVARD, STANFORD"
                    required
                  />
                  <p className="text-xs text-gray-500 mt-1">This ID will be used for student ID generation: {profile.institute_id}-00001</p>
                </div>
              </div>

              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700">Email</label>
                  <input
                    type="email"
                    value={profile.email}
                    onChange={(e) => setProfile({...profile, email: e.target.value})}
                    className="mt-1 w-full px-3 py-2 border rounded-md"
                    required
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700">Location</label>
                  <input
                    type="text"
                    value={profile.location || ''}
                    onChange={(e) => setProfile({...profile, location: e.target.value})}
                    className="mt-1 w-full px-3 py-2 border rounded-md"
                    placeholder="City, Country"
                  />
                </div>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700">Description</label>
                <textarea
                  value={profile.description || ''}
                  onChange={(e) => setProfile({...profile, description: e.target.value})}
                  rows={3}
                  className="mt-1 w-full px-3 py-2 border rounded-md"
                  placeholder="Brief description about your institute..."
                />
              </div>

              <div className="flex space-x-3">
                <button type="submit" className="px-4 py-2 bg-green-600 text-white rounded hover:bg-green-700">
                  Save Changes
                </button>
                <button type="button" onClick={() => setEditingProfile(false)} className="px-4 py-2 bg-gray-500 text-white rounded hover:bg-gray-600">
                  Cancel
                </button>
              </div>
            </form>
          )}
        </div>
      )}
    </div>
  );

  const renderStudents = () => (
    <div className="space-y-6">
      <h3 className="text-lg font-semibold">Manage Students</h3>
      
      <form onSubmit={handleAddStudent} className="bg-gray-50 p-4 rounded-lg space-y-3">
        <h4 className="font-medium">Add New Student</h4>
        <div className="bg-blue-50 p-3 rounded text-sm text-blue-800">
          <strong>Note:</strong> Student ID will be auto-generated as [{profile?.institute_id || 'INSTITUTEID'}-00001] format
        </div>
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
          Add Student (Auto-Generate ID)
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
                {editingStudent === student.id ? (
                  <div className="space-y-3">
                    <div className="bg-yellow-50 p-2 rounded text-sm text-yellow-800">
                      <strong>Note:</strong> Student ID cannot be changed: <span className="font-mono">{student.student_id}</span>
                    </div>
                    <input
                      type="text"
                      defaultValue={student.name}
                      placeholder="Full Name"
                      className="w-full px-3 py-2 border rounded-md"
                      id={`name-${student.id}`}
                    />
                    <input
                      type="email"
                      defaultValue={student.email}
                      placeholder="Email"
                      className="w-full px-3 py-2 border rounded-md"
                      id={`email-${student.id}`}
                    />
                    <div className="flex space-x-2">
                      <button
                        onClick={() => handleEditStudent(student.id, {
                          name: document.getElementById(`name-${student.id}`).value,
                          email: document.getElementById(`email-${student.id}`).value
                        })}
                        className="px-3 py-1 bg-green-600 text-white rounded hover:bg-green-700 text-sm"
                      >
                        Save
                      </button>
                      <button
                        onClick={() => setEditingStudent(null)}
                        className="px-3 py-1 bg-gray-500 text-white rounded hover:bg-gray-600 text-sm"
                      >
                        Cancel
                      </button>
                    </div>
                  </div>
                ) : (
                  <div className="flex justify-between items-start">
                    <div>
                      <p className="font-medium">{student.name}</p>
                      <p className="text-sm text-gray-600">ID: <span className="font-mono bg-gray-100 px-2 py-1 rounded">{student.student_id}</span></p>
                      <p className="text-sm text-gray-600">Email: {student.email}</p>
                    </div>
                    <button
                      onClick={() => setEditingStudent(student.id)}
                      className="px-3 py-1 bg-blue-500 text-white rounded hover:bg-blue-600 text-sm"
                    >
                      Edit
                    </button>
                  </div>
                )}
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
                { key: 'profile', label: 'Profile' },
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
              {activeTab === 'profile' && renderProfile()}
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