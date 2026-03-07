import React, { useState } from 'react';
import { useAuth } from '../contexts/AuthContext';

const LoginForm = () => {
  const [userType, setUserType] = useState('admin');
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [email, setEmail] = useState('');
  const [instituteName, setInstituteName] = useState('');
  const [location, setLocation] = useState('');
  const [studentId, setStudentId] = useState('');
  const [name, setName] = useState('');
  const [isRegister, setIsRegister] = useState(false);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  
  const { login } = useAuth();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');

    try {
      let endpoint, body;

      if (userType === 'admin') {
        endpoint = '/auth/admin/login';
        body = { username, password };
      } else if (userType === 'institute') {
        if (isRegister) {
          endpoint = '/auth/institute/register';
          body = { institute_name: instituteName, username, password, email, location };
        } else {
          endpoint = '/auth/institute/login';
          body = { username: email, password };
        }
      } else if (userType === 'student') {
        if (isRegister) {
          endpoint = '/auth/student/register';
          body = { student_id: studentId, name, email, password };
        } else {
          endpoint = '/auth/student/login';
          body = { username: studentId, password };
        }
      } else if (userType === 'verifier') {
        if (isRegister) {
          endpoint = '/auth/verifier/register';
          body = { username, password, email };
        } else {
          endpoint = '/auth/verifier/login';
          body = { username, password };
        }
      }

      const response = await fetch(`http://localhost:8000${endpoint}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(body)
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.detail || 'Authentication failed');
      }

      if (isRegister) {
        setIsRegister(false);
        setError('Registration successful! Please login.');
      } else {
        login(data.access_token, data.role);
      }
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-blue-50 to-indigo-100">
      <div className="max-w-md w-full space-y-8 bg-white p-8 rounded-lg shadow-lg">
        <div>
          <h2 className="text-center text-3xl font-extrabold text-gray-900">CertiSense AI</h2>
          <p className="mt-2 text-center text-sm text-gray-600">Enhanced Blockchain Certificate System</p>
        </div>
        
        <form className="mt-8 space-y-6" onSubmit={handleSubmit}>
          <div className="mb-4">
            <label className="block text-sm font-medium text-gray-700 mb-2">User Type</label>
            <select
              value={userType}
              onChange={(e) => setUserType(e.target.value)}
              className="w-full px-3 py-2 border border-gray-300 rounded-md"
            >
              <option value="admin">Admin</option>
              <option value="institute">Institute</option>
              <option value="student">Student</option>
              <option value="verifier">Verifier</option>
            </select>
          </div>

          {userType === 'admin' && (
            <>
              <input type="text" value={username} onChange={(e) => setUsername(e.target.value)} placeholder="Username" className="w-full px-3 py-2 border border-gray-300 rounded-md" required />
              <input type="password" value={password} onChange={(e) => setPassword(e.target.value)} placeholder="Password" className="w-full px-3 py-2 border border-gray-300 rounded-md" required />
            </>
          )}

          {userType === 'institute' && (
            <>
              {isRegister && (
                <>
                  <input type="text" value={instituteName} onChange={(e) => setInstituteName(e.target.value)} placeholder="Institute Name" className="w-full px-3 py-2 border border-gray-300 rounded-md" required />
                  <input type="text" value={location} onChange={(e) => setLocation(e.target.value)} placeholder="Location" className="w-full px-3 py-2 border border-gray-300 rounded-md" />
                </>
              )}
              <input type="email" value={email} onChange={(e) => setEmail(e.target.value)} placeholder="Email" className="w-full px-3 py-2 border border-gray-300 rounded-md" required />
              <input type="password" value={password} onChange={(e) => setPassword(e.target.value)} placeholder="Password" className="w-full px-3 py-2 border border-gray-300 rounded-md" required />
            </>
          )}

          {userType === 'student' && (
            <>
              <input type="text" value={studentId} onChange={(e) => setStudentId(e.target.value)} placeholder="Student ID" className="w-full px-3 py-2 border border-gray-300 rounded-md" required />
              {isRegister && (
                <>
                  <input type="text" value={name} onChange={(e) => setName(e.target.value)} placeholder="Full Name" className="w-full px-3 py-2 border border-gray-300 rounded-md" required />
                  <input type="email" value={email} onChange={(e) => setEmail(e.target.value)} placeholder="Email" className="w-full px-3 py-2 border border-gray-300 rounded-md" required />
                </>
              )}
              <input type="password" value={password} onChange={(e) => setPassword(e.target.value)} placeholder="Password" className="w-full px-3 py-2 border border-gray-300 rounded-md" required />
            </>
          )}

          {userType === 'verifier' && (
            <>
              <input type="text" value={username} onChange={(e) => setUsername(e.target.value)} placeholder="Username" className="w-full px-3 py-2 border border-gray-300 rounded-md" required />
              {isRegister && <input type="email" value={email} onChange={(e) => setEmail(e.target.value)} placeholder="Email" className="w-full px-3 py-2 border border-gray-300 rounded-md" required />}
              <input type="password" value={password} onChange={(e) => setPassword(e.target.value)} placeholder="Password" className="w-full px-3 py-2 border border-gray-300 rounded-md" required />
            </>
          )}

          {error && <div className="text-red-600 text-sm text-center">{error}</div>}

          <button type="submit" disabled={loading} className="w-full py-2 px-4 bg-indigo-600 text-white rounded-md hover:bg-indigo-700 disabled:opacity-50">
            {loading ? 'Processing...' : (isRegister ? 'Register' : 'Sign In')}
          </button>

          {(userType === 'institute' || userType === 'student' || userType === 'verifier') && (
            <button type="button" onClick={() => setIsRegister(!isRegister)} className="w-full text-indigo-600 hover:text-indigo-500 text-sm">
              {isRegister ? 'Already have an account? Sign in' : 'Need an account? Register'}
            </button>
          )}
        </form>
      </div>
    </div>
  );
};

export default LoginForm;