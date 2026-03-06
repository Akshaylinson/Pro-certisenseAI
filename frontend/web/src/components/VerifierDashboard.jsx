import React, { useState, useEffect } from 'react';
import axios from 'axios';

const API_URL = 'http://localhost:8000';

const VerifierDashboard = () => {
  const [activeModule, setActiveModule] = useState('dashboard');
  const [dashboardStats, setDashboardStats] = useState(null);
  const [verificationResult, setVerificationResult] = useState(null);
  const [history, setHistory] = useState([]);
  const [feedbacks, setFeedbacks] = useState([]);
  const [chatMessages, setChatMessages] = useState([]);
  const [chatInput, setChatInput] = useState('');
  const [loading, setLoading] = useState(false);

  const token = localStorage.getItem('verifier_token');
  const headers = { Authorization: `Bearer ${token}` };

  useEffect(() => {
    if (activeModule === 'dashboard') loadDashboard();
    else if (activeModule === 'history') loadHistory();
    else if (activeModule === 'feedback') loadFeedbacks();
  }, [activeModule]);

  const loadDashboard = async () => {
    try {
      const res = await axios.get(`${API_URL}/verifier/dashboard`, { headers });
      setDashboardStats(res.data);
    } catch (err) {
      console.error(err);
    }
  };

  const loadHistory = async () => {
    try {
      const res = await axios.get(`${API_URL}/verifier/history`, { headers });
      setHistory(res.data.history);
    } catch (err) {
      console.error(err);
    }
  };

  const loadFeedbacks = async () => {
    try {
      const res = await axios.get(`${API_URL}/verifier/feedback`, { headers });
      setFeedbacks(res.data.feedbacks);
    } catch (err) {
      console.error(err);
    }
  };

  const handleVerifyCertificate = async (e) => {
    e.preventDefault();
    const file = e.target.certificate.files[0];
    if (!file) return;

    setLoading(true);
    const formData = new FormData();
    formData.append('file', file);

    try {
      const res = await axios.post(`${API_URL}/verifier/verify`, formData, { headers });
      setVerificationResult(res.data);
      alert(`Verification Result: ${res.data.verification_result.toUpperCase()}`);
    } catch (err) {
      alert('Verification failed: ' + (err.response?.data?.detail || 'Error'));
    }
    setLoading(false);
  };

  const generateProof = async (verificationId) => {
    try {
      const res = await axios.post(`${API_URL}/verifier/proof/generate/${verificationId}`, {}, { headers });
      alert('Proof generated successfully!');
      console.log('Proof:', res.data);
    } catch (err) {
      alert('Proof generation failed');
    }
  };

  const viewAIAnalysis = async (verificationId) => {
    try {
      const res = await axios.get(`${API_URL}/verifier/ai-analysis/${verificationId}`, { headers });
      alert(`AI Analysis:\nConfidence: ${(res.data.confidence_score * 100).toFixed(1)}%\nResult: ${res.data.ai_validation_result}`);
    } catch (err) {
      alert('Failed to load AI analysis');
    }
  };

  const viewBlockchainDetails = async (certHash) => {
    try {
      const res = await axios.get(`${API_URL}/verifier/blockchain/${certHash}`, { headers });
      alert(`Blockchain Details:\nHash: ${res.data.blockchain_hash}\nStatus: ${res.data.status}\nValid: ${res.data.valid}`);
    } catch (err) {
      alert('Failed to load blockchain details');
    }
  };

  const submitFeedback = async (e) => {
    e.preventDefault();
    const formDataObj = new FormData(e.target);
    
    const formData = new FormData();
    formData.append('feedback_type', formDataObj.get('type'));
    formData.append('message', formDataObj.get('message'));
    formData.append('priority', formDataObj.get('priority'));
    
    try {
      await axios.post(`${API_URL}/verifier/feedback`, formData, {
        headers: {
          ...headers,
          'Content-Type': 'multipart/form-data'
        }
      });
      alert('Feedback submitted successfully');
      e.target.reset();
      loadFeedbacks();
    } catch (err) {
      alert('Feedback submission failed');
    }
  };

  const sendChatMessage = async () => {
    if (!chatInput.trim()) return;

    const userMessage = { role: 'user', content: chatInput };
    setChatMessages([...chatMessages, userMessage]);

    try {
      const res = await axios.post(`${API_URL}/verifier/chatbot?message=${encodeURIComponent(chatInput)}`, {}, { headers });
      const botMessage = { role: 'bot', content: res.data.response };
      setChatMessages([...chatMessages, userMessage, botMessage]);
    } catch (err) {
      const errorMessage = { role: 'bot', content: 'Sorry, I encountered an error.' };
      setChatMessages([...chatMessages, userMessage, errorMessage]);
    }

    setChatInput('');
  };

  const handleLogout = () => {
    localStorage.removeItem('verifier_token');
    window.location.href = '/';
  };

  return (
    <div className="min-h-screen bg-gray-100">
      {/* Navigation */}
      <nav className="bg-green-600 text-white shadow-lg">
        <div className="container mx-auto px-4 py-4 flex justify-between items-center">
          <div>
            <h1 className="text-2xl font-bold">🔍 CertiSense Verifier</h1>
            <p className="text-sm text-green-200">Certificate Verification Platform</p>
          </div>
          <button onClick={handleLogout} className="bg-red-500 hover:bg-red-600 px-6 py-2 rounded-lg font-semibold transition">
            Logout
          </button>
        </div>
      </nav>

      <div className="container mx-auto mt-6 px-4">
        <div className="flex gap-6">
          {/* Sidebar */}
          <div className="w-64 bg-white rounded-lg shadow-lg p-4 h-fit">
            <h2 className="font-bold text-lg mb-4 text-gray-700">Verifier Modules</h2>
            <ul className="space-y-2">
              {[
                { id: 'dashboard', label: '📊 Dashboard' },
                { id: 'verify', label: '✅ Verify Certificate' },
                { id: 'history', label: '📜 History' },
                { id: 'feedback', label: '💬 Feedback' },
                { id: 'chatbot', label: '🤖 Chatbot' }
              ].map(mod => (
                <li key={mod.id}>
                  <button
                    onClick={() => setActiveModule(mod.id)}
                    className={`w-full text-left px-4 py-3 rounded-lg transition ${
                      activeModule === mod.id ? 'bg-green-500 text-white shadow-md' : 'hover:bg-gray-100 text-gray-700'
                    }`}
                  >
                    {mod.label}
                  </button>
                </li>
              ))}
            </ul>
          </div>

          {/* Main Content */}
          <div className="flex-1 bg-white rounded-lg shadow-lg p-6">
            {/* MODULE 1: Dashboard */}
            {activeModule === 'dashboard' && dashboardStats && (
              <div>
                <h2 className="text-3xl font-bold mb-6 text-gray-800">Verifier Dashboard</h2>
                
                <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
                  <div className="bg-gradient-to-br from-green-400 to-green-600 text-white p-6 rounded-lg shadow">
                    <h3 className="text-sm font-semibold mb-2">Total Verifications</h3>
                    <p className="text-4xl font-bold">{dashboardStats.statistics.total_verifications}</p>
                  </div>
                  <div className="bg-gradient-to-br from-blue-400 to-blue-600 text-white p-6 rounded-lg shadow">
                    <h3 className="text-sm font-semibold mb-2">Valid Certificates</h3>
                    <p className="text-4xl font-bold">{dashboardStats.statistics.valid_certificates}</p>
                  </div>
                  <div className="bg-gradient-to-br from-purple-400 to-purple-600 text-white p-6 rounded-lg shadow">
                    <h3 className="text-sm font-semibold mb-2">Success Rate</h3>
                    <p className="text-4xl font-bold">{dashboardStats.success_rate.toFixed(1)}%</p>
                  </div>
                </div>

                <div className="grid grid-cols-2 gap-4">
                  <div className="bg-red-50 p-4 rounded-lg border border-red-200">
                    <h3 className="font-bold mb-2">Invalid Certificates</h3>
                    <p className="text-2xl font-bold text-red-600">{dashboardStats.statistics.invalid_certificates}</p>
                  </div>
                  <div className="bg-orange-50 p-4 rounded-lg border border-orange-200">
                    <h3 className="font-bold mb-2">Tampered Certificates</h3>
                    <p className="text-2xl font-bold text-orange-600">{dashboardStats.statistics.tampered_certificates}</p>
                  </div>
                </div>
              </div>
            )}

            {/* MODULE 2: Verify Certificate */}
            {activeModule === 'verify' && (
              <div>
                <h2 className="text-3xl font-bold mb-6 text-gray-800">Verify Certificate</h2>
                
                <form onSubmit={handleVerifyCertificate} className="space-y-6">
                  <div className="border-2 border-dashed border-gray-300 rounded-lg p-8 text-center">
                    <input
                      type="file"
                      name="certificate"
                      accept=".pdf,.jpg,.jpeg,.png"
                      className="block w-full text-sm text-gray-500 file:mr-4 file:py-2 file:px-4 file:rounded-lg file:border-0 file:text-sm file:font-semibold file:bg-green-50 file:text-green-700 hover:file:bg-green-100"
                      required
                    />
                    <p className="mt-2 text-sm text-gray-500">Upload certificate (PDF, JPG, PNG)</p>
                  </div>

                  <button
                    type="submit"
                    disabled={loading}
                    className={`w-full py-3 rounded-lg font-semibold text-white transition ${
                      loading ? 'bg-gray-400' : 'bg-green-600 hover:bg-green-700'
                    }`}
                  >
                    {loading ? 'Verifying...' : 'Verify Certificate'}
                  </button>
                </form>

                {verificationResult && (
                  <div className="mt-6 bg-gray-50 p-6 rounded-lg border">
                    <h3 className="font-bold text-lg mb-4">Verification Result</h3>
                    <div className="space-y-2">
                      <p><strong>Result:</strong> <span className={`px-3 py-1 rounded ${
                        verificationResult.verification_result === 'valid' ? 'bg-green-100 text-green-800' :
                        verificationResult.verification_result === 'invalid' ? 'bg-red-100 text-red-800' :
                        'bg-orange-100 text-orange-800'
                      }`}>{verificationResult.verification_result.toUpperCase()}</span></p>
                      <p><strong>Confidence:</strong> {(verificationResult.confidence_score * 100).toFixed(1)}%</p>
                      <p><strong>Blockchain Verified:</strong> {verificationResult.blockchain_verified ? '✅ Yes' : '❌ No'}</p>
                      <p><strong>Processing Time:</strong> {verificationResult.processing_time.toFixed(2)}s</p>
                      
                      <div className="mt-4 flex gap-2">
                        <button
                          onClick={() => generateProof(verificationResult.verification_id)}
                          className="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600"
                        >
                          Generate Proof
                        </button>
                        <button
                          onClick={() => viewAIAnalysis(verificationResult.verification_id)}
                          className="bg-purple-500 text-white px-4 py-2 rounded hover:bg-purple-600"
                        >
                          AI Analysis
                        </button>
                        <button
                          onClick={() => viewBlockchainDetails(verificationResult.certificate_hash)}
                          className="bg-indigo-500 text-white px-4 py-2 rounded hover:bg-indigo-600"
                        >
                          Blockchain Details
                        </button>
                      </div>
                    </div>
                  </div>
                )}
              </div>
            )}

            {/* MODULE 3: Verification History */}
            {activeModule === 'history' && (
              <div>
                <h2 className="text-3xl font-bold mb-6 text-gray-800">Verification History</h2>
                
                <div className="overflow-x-auto">
                  <table className="w-full border-collapse">
                    <thead>
                      <tr className="bg-gray-200">
                        <th className="p-3 text-left">Verification ID</th>
                        <th className="p-3 text-left">Certificate Hash</th>
                        <th className="p-3 text-center">Result</th>
                        <th className="p-3 text-center">Confidence</th>
                        <th className="p-3 text-left">Timestamp</th>
                      </tr>
                    </thead>
                    <tbody>
                      {history.map(h => (
                        <tr key={h.verification_id} className="border-b hover:bg-gray-50">
                          <td className="p-3 font-mono text-xs">{h.verification_id.slice(0, 12)}...</td>
                          <td className="p-3 font-mono text-xs">{h.certificate_hash}</td>
                          <td className="p-3 text-center">
                            <span className={`px-2 py-1 rounded text-xs ${
                              h.verification_result === 'valid' ? 'bg-green-100 text-green-800' :
                              h.verification_result === 'invalid' ? 'bg-red-100 text-red-800' :
                              'bg-orange-100 text-orange-800'
                            }`}>
                              {h.verification_result}
                            </span>
                          </td>
                          <td className="p-3 text-center">{(h.confidence_score * 100).toFixed(1)}%</td>
                          <td className="p-3 text-sm">{new Date(h.timestamp).toLocaleString()}</td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              </div>
            )}

            {/* MODULE 4: Submit Feedback */}
            {activeModule === 'feedback' && (
              <div>
                <h2 className="text-3xl font-bold mb-6 text-gray-800">Submit Feedback</h2>
                
                <form onSubmit={submitFeedback} className="space-y-4 mb-8">
                  <div>
                    <label className="block font-semibold mb-2">Feedback Type</label>
                    <select name="type" className="w-full px-4 py-2 border rounded-lg" required>
                      <option value="suspicious">Suspicious Certificate</option>
                      <option value="issue">Verification Issue</option>
                      <option value="general">General Feedback</option>
                    </select>
                  </div>

                  <div>
                    <label className="block font-semibold mb-2">Priority</label>
                    <select name="priority" className="w-full px-4 py-2 border rounded-lg">
                      <option value="low">Low</option>
                      <option value="medium">Medium</option>
                      <option value="high">High</option>
                    </select>
                  </div>

                  <div>
                    <label className="block font-semibold mb-2">Message</label>
                    <textarea
                      name="message"
                      rows="4"
                      className="w-full px-4 py-2 border rounded-lg"
                      placeholder="Describe your feedback..."
                      required
                    ></textarea>
                  </div>

                  <button type="submit" className="bg-green-600 text-white px-6 py-2 rounded-lg hover:bg-green-700">
                    Submit Feedback
                  </button>
                </form>

                <h3 className="font-bold text-xl mb-4">My Feedback</h3>
                <div className="space-y-3">
                  {feedbacks.map(fb => (
                    <div key={fb.id} className="bg-gray-50 p-4 rounded-lg border">
                      <div className="flex justify-between items-start">
                        <div>
                          <p className="font-semibold">{fb.feedback_type}</p>
                          <p className="text-sm text-gray-600">{fb.message}</p>
                        </div>
                        <span className={`px-2 py-1 rounded text-xs ${
                          fb.priority === 'high' ? 'bg-red-100 text-red-800' :
                          fb.priority === 'medium' ? 'bg-yellow-100 text-yellow-800' :
                          'bg-green-100 text-green-800'
                        }`}>
                          {fb.priority}
                        </span>
                      </div>
                      <p className="text-xs text-gray-500 mt-2">{new Date(fb.timestamp).toLocaleString()}</p>
                    </div>
                  ))}
                </div>
              </div>
            )}

            {/* MODULE 5: Chatbot */}
            {activeModule === 'chatbot' && (
              <div>
                <h2 className="text-3xl font-bold mb-6 text-gray-800">Verification Assistant</h2>
                
                <div className="bg-gray-50 rounded-lg p-4 h-96 overflow-y-auto mb-4">
                  {chatMessages.map((msg, idx) => (
                    <div key={idx} className={`mb-3 ${msg.role === 'user' ? 'text-right' : 'text-left'}`}>
                      <div className={`inline-block px-4 py-2 rounded-lg ${
                        msg.role === 'user' ? 'bg-green-500 text-white' : 'bg-gray-200 text-gray-800'
                      }`}>
                        {msg.content}
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
                    className="flex-1 px-4 py-2 border rounded-lg"
                    placeholder="Ask about certificate verification..."
                  />
                  <button
                    onClick={sendChatMessage}
                    className="bg-green-600 text-white px-6 py-2 rounded-lg hover:bg-green-700"
                  >
                    Send
                  </button>
                </div>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default VerifierDashboard;
