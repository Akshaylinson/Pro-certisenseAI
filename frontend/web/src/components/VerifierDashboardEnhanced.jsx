import React, { useState, useEffect } from 'react';
import axios from 'axios';

const API_URL = 'http://localhost:8000/api/verifier';

const VerifierDashboardEnhanced = () => {
  const [activeModule, setActiveModule] = useState('dashboard');
  const [dashboardStats, setDashboardStats] = useState(null);
  const [verificationResult, setVerificationResult] = useState(null);
  const [history, setHistory] = useState([]);
  const [feedbacks, setFeedbacks] = useState([]);
  const [chatMessages, setChatMessages] = useState([]);
  const [chatInput, setChatInput] = useState('');
  const [loading, setLoading] = useState(false);
  const [filterStatus, setFilterStatus] = useState('');
  const [selectedVerification, setSelectedVerification] = useState(null);

  const token = localStorage.getItem('token');
  const headers = { Authorization: `Bearer ${token}` };

  useEffect(() => {
    if (activeModule === 'dashboard') loadDashboard();
    else if (activeModule === 'history') loadHistory();
    else if (activeModule === 'feedback') loadFeedbacks();
  }, [activeModule]);

  const loadDashboard = async () => {
    try {
      const res = await axios.get(`${API_URL}/dashboard`, { headers });
      setDashboardStats(res.data);
    } catch (err) {
      console.error('Dashboard load error:', err);
    }
  };

  const loadHistory = async () => {
    try {
      const params = filterStatus ? { status: filterStatus } : {};
      const res = await axios.get(`${API_URL}/history`, { headers, params });
      setHistory(res.data.history);
    } catch (err) {
      console.error('History load error:', err);
    }
  };

  const loadFeedbacks = async () => {
    try {
      const res = await axios.get(`${API_URL}/feedback`, { headers });
      setFeedbacks(res.data.feedbacks);
    } catch (err) {
      console.error('Feedback load error:', err);
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
      const res = await axios.post(`${API_URL}/verify`, formData, { headers });
      setVerificationResult(res.data);
      alert(`✅ Verification Complete!\nResult: ${res.data.verification_result.toUpperCase()}\nConfidence: ${(res.data.confidence_score * 100).toFixed(1)}%`);
    } catch (err) {
      alert('❌ Verification failed: ' + (err.response?.data?.detail || 'Error'));
    }
    setLoading(false);
  };

  const generateProof = async (verificationId) => {
    try {
      const res = await axios.post(`${API_URL}/proof/generate/${verificationId}`, {}, { headers });
      alert('✅ Verification Proof Generated!\n\nProof Hash: ' + res.data.proof_hash.substring(0, 16) + '...');
      
      // Download proof
      const proofData = JSON.stringify(res.data.report, null, 2);
      const blob = new Blob([proofData], { type: 'application/json' });
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `verification_proof_${verificationId}.json`;
      a.click();
    } catch (err) {
      alert('❌ Proof generation failed');
    }
  };

  const viewAIAnalysis = async (verificationId) => {
    try {
      const res = await axios.get(`${API_URL}/ai-analysis/${verificationId}`, { headers });
      const analysis = res.data;
      
      let message = `🤖 AI Verification Analysis\n\n`;
      message += `Result: ${analysis.ai_validation_result.toUpperCase()}\n`;
      message += `Confidence: ${(analysis.confidence_score * 100).toFixed(1)}%\n`;
      message += `Risk Level: ${analysis.risk_level.toUpperCase()}\n`;
      message += `AI Model: ${analysis.ai_model}\n\n`;
      
      if (analysis.fraud_indicators.length > 0) {
        message += `⚠️ Fraud Indicators:\n`;
        analysis.fraud_indicators.forEach(indicator => {
          message += `• ${indicator}\n`;
        });
      } else {
        message += `✅ No fraud indicators detected`;
      }
      
      alert(message);
    } catch (err) {
      alert('❌ Failed to load AI analysis');
    }
  };

  const viewBlockchainDetails = async (certHash) => {
    try {
      const res = await axios.get(`${API_URL}/blockchain/${certHash}`, { headers });
      const blockchain = res.data;
      
      let message = `⛓️ Blockchain Details\n\n`;
      message += `Certificate Hash: ${blockchain.certificate_hash.substring(0, 20)}...\n`;
      message += `Blockchain Hash: ${blockchain.blockchain_hash?.substring(0, 20)}...\n`;
      message += `Status: ${blockchain.status}\n`;
      message += `Valid: ${blockchain.valid ? '✅ Yes' : '❌ No'}\n`;
      message += `Issuer: ${blockchain.issuer_id}\n`;
      message += `Student: ${blockchain.student_id}\n`;
      message += `Network: ${blockchain.network}\n`;
      message += `Verifications: ${blockchain.verifications.length}`;
      
      alert(message);
    } catch (err) {
      alert('❌ Failed to load blockchain details');
    }
  };

  const submitFeedback = async (e) => {
    e.preventDefault();
    const formData = new FormData(e.target);
    
    try {
      await axios.post(
        `${API_URL}/feedback?feedback_type=${formData.get('type')}&message=${encodeURIComponent(formData.get('message'))}&priority=${formData.get('priority')}`,
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

  const sendChatMessage = async () => {
    if (!chatInput.trim()) return;

    const userMessage = { role: 'user', content: chatInput };
    setChatMessages([...chatMessages, userMessage]);

    try {
      const res = await axios.post(
        `${API_URL}/chatbot?message=${encodeURIComponent(chatInput)}`,
        {},
        { headers }
      );
      const botMessage = { role: 'bot', content: res.data.response || 'Response received' };
      setChatMessages([...chatMessages, userMessage, botMessage]);
    } catch (err) {
      const errorMessage = { role: 'bot', content: 'Sorry, I encountered an error.' };
      setChatMessages([...chatMessages, userMessage, errorMessage]);
    }

    setChatInput('');
  };

  const handleLogout = () => {
    localStorage.removeItem('token');
    window.location.href = '/';
  };

  const getStatusColor = (status) => {
    switch (status) {
      case 'valid': return 'bg-green-100 text-green-800';
      case 'invalid': return 'bg-red-100 text-red-800';
      case 'tampered': return 'bg-orange-100 text-orange-800';
      case 'revoked': return 'bg-gray-100 text-gray-800';
      default: return 'bg-blue-100 text-blue-800';
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-50 to-gray-100">
      {/* Navigation */}
      <nav className="bg-gradient-to-r from-green-600 to-green-700 text-white shadow-xl">
        <div className="container mx-auto px-6 py-4 flex justify-between items-center">
          <div>
            <h1 className="text-3xl font-bold flex items-center gap-2">
              🔍 CertiSense Verifier
            </h1>
            <p className="text-sm text-green-100 mt-1">Blockchain Certificate Verification Platform v3.0</p>
          </div>
          <button 
            onClick={handleLogout} 
            className="bg-red-500 hover:bg-red-600 px-6 py-2 rounded-lg font-semibold transition shadow-lg"
          >
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
                { id: 'dashboard', label: '📊 Dashboard', desc: 'Overview & Stats' },
                { id: 'verify', label: '✅ Verify Certificate', desc: 'Upload & Verify' },
                { id: 'history', label: '📜 History', desc: 'Past Verifications' },
                { id: 'feedback', label: '💬 Feedback', desc: 'Submit Issues' },
                { id: 'chatbot', label: '🤖 AI Assistant', desc: 'Get Help' }
              ].map(mod => (
                <li key={mod.id}>
                  <button
                    onClick={() => setActiveModule(mod.id)}
                    className={`w-full text-left px-4 py-3 rounded-lg transition shadow-sm ${
                      activeModule === mod.id 
                        ? 'bg-gradient-to-r from-green-500 to-green-600 text-white shadow-lg transform scale-105' 
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
                <h2 className="text-4xl font-bold mb-8 text-gray-800 flex items-center gap-3">
                  📊 Verifier Dashboard
                </h2>
                
                <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
                  <div className="bg-gradient-to-br from-green-400 to-green-600 text-white p-6 rounded-xl shadow-lg">
                    <h3 className="text-sm font-semibold mb-2 opacity-90">Total Verifications</h3>
                    <p className="text-5xl font-bold">{dashboardStats.statistics.total_verifications}</p>
                  </div>
                  <div className="bg-gradient-to-br from-blue-400 to-blue-600 text-white p-6 rounded-xl shadow-lg">
                    <h3 className="text-sm font-semibold mb-2 opacity-90">Valid Certificates</h3>
                    <p className="text-5xl font-bold">{dashboardStats.statistics.valid_certificates}</p>
                  </div>
                  <div className="bg-gradient-to-br from-purple-400 to-purple-600 text-white p-6 rounded-xl shadow-lg">
                    <h3 className="text-sm font-semibold mb-2 opacity-90">Success Rate</h3>
                    <p className="text-5xl font-bold">{dashboardStats.success_rate}%</p>
                  </div>
                </div>

                <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-8">
                  <div className="bg-red-50 p-5 rounded-xl border-2 border-red-200">
                    <h3 className="font-bold mb-2 text-gray-700">Invalid</h3>
                    <p className="text-3xl font-bold text-red-600">{dashboardStats.statistics.invalid_certificates}</p>
                  </div>
                  <div className="bg-orange-50 p-5 rounded-xl border-2 border-orange-200">
                    <h3 className="font-bold mb-2 text-gray-700">Tampered</h3>
                    <p className="text-3xl font-bold text-orange-600">{dashboardStats.statistics.tampered_certificates}</p>
                  </div>
                  <div className="bg-gray-50 p-5 rounded-xl border-2 border-gray-200">
                    <h3 className="font-bold mb-2 text-gray-700">Revoked</h3>
                    <p className="text-3xl font-bold text-gray-600">{dashboardStats.statistics.revoked_certificates}</p>
                  </div>
                  <div className="bg-indigo-50 p-5 rounded-xl border-2 border-indigo-200">
                    <h3 className="font-bold mb-2 text-gray-700">Recent (30d)</h3>
                    <p className="text-3xl font-bold text-indigo-600">{dashboardStats.statistics.recent_verifications_30d}</p>
                  </div>
                </div>

                {dashboardStats.performance && (
                  <div className="bg-gradient-to-r from-indigo-50 to-purple-50 p-6 rounded-xl border border-indigo-200">
                    <h3 className="font-bold text-lg mb-4 text-gray-800">📈 Performance Metrics</h3>
                    <div className="grid grid-cols-2 gap-4">
                      <div>
                        <p className="text-sm text-gray-600">Average Confidence</p>
                        <p className="text-2xl font-bold text-indigo-600">{dashboardStats.performance.avg_confidence}%</p>
                      </div>
                      <div>
                        <p className="text-sm text-gray-600">Blockchain Verification Rate</p>
                        <p className="text-2xl font-bold text-purple-600">{dashboardStats.performance.blockchain_verification_rate}%</p>
                      </div>
                    </div>
                  </div>
                )}
              </div>
            )}

            {/* Verify Certificate Module */}
            {activeModule === 'verify' && (
              <div>
                <h2 className="text-4xl font-bold mb-8 text-gray-800 flex items-center gap-3">
                  ✅ Verify Certificate
                </h2>
                
                <form onSubmit={handleVerifyCertificate} className="space-y-6">
                  <div className="border-2 border-dashed border-green-300 rounded-xl p-10 text-center bg-green-50 hover:bg-green-100 transition">
                    <div className="text-6xl mb-4">📄</div>
                    <input
                      type="file"
                      name="certificate"
                      accept=".pdf,.jpg,.jpeg,.png"
                      className="block w-full text-sm text-gray-600 file:mr-4 file:py-3 file:px-6 file:rounded-lg file:border-0 file:text-sm file:font-semibold file:bg-green-600 file:text-white hover:file:bg-green-700 file:cursor-pointer"
                      required
                    />
                    <p className="mt-4 text-sm text-gray-600">Supported formats: PDF, JPG, PNG (Max 10MB)</p>
                  </div>

                  <button
                    type="submit"
                    disabled={loading}
                    className={`w-full py-4 rounded-xl font-bold text-white text-lg transition shadow-lg ${
                      loading ? 'bg-gray-400 cursor-not-allowed' : 'bg-gradient-to-r from-green-600 to-green-700 hover:from-green-700 hover:to-green-800'
                    }`}
                  >
                    {loading ? '🔄 Verifying...' : '🔍 Verify Certificate'}
                  </button>
                </form>

                {verificationResult && (
                  <div className="mt-8 bg-gradient-to-r from-gray-50 to-gray-100 p-8 rounded-xl border-2 border-gray-200 shadow-lg">
                    <h3 className="font-bold text-2xl mb-6 text-gray-800">📋 Verification Result</h3>
                    <div className="space-y-4">
                      <div className="flex justify-between items-center">
                        <span className="font-semibold text-gray-700">Result:</span>
                        <span className={`px-4 py-2 rounded-lg font-bold ${getStatusColor(verificationResult.verification_result)}`}>
                          {verificationResult.verification_result.toUpperCase()}
                        </span>
                      </div>
                      <div className="flex justify-between items-center">
                        <span className="font-semibold text-gray-700">Confidence Score:</span>
                        <span className="text-xl font-bold text-green-600">{(verificationResult.confidence_score * 100).toFixed(1)}%</span>
                      </div>
                      <div className="flex justify-between items-center">
                        <span className="font-semibold text-gray-700">Blockchain Verified:</span>
                        <span className="text-xl">{verificationResult.blockchain_verified ? '✅ Yes' : '❌ No'}</span>
                      </div>
                      <div className="flex justify-between items-center">
                        <span className="font-semibold text-gray-700">Processing Time:</span>
                        <span className="text-lg text-gray-600">{verificationResult.processing_time.toFixed(2)}s</span>
                      </div>
                      
                      <div className="mt-6 flex gap-3 flex-wrap">
                        <button
                          onClick={() => generateProof(verificationResult.verification_id)}
                          className="flex-1 bg-blue-500 text-white px-6 py-3 rounded-lg hover:bg-blue-600 font-semibold shadow-md transition"
                        >
                          📥 Generate Proof
                        </button>
                        <button
                          onClick={() => viewAIAnalysis(verificationResult.verification_id)}
                          className="flex-1 bg-purple-500 text-white px-6 py-3 rounded-lg hover:bg-purple-600 font-semibold shadow-md transition"
                        >
                          🤖 AI Analysis
                        </button>
                        <button
                          onClick={() => viewBlockchainDetails(verificationResult.certificate_hash)}
                          className="flex-1 bg-indigo-500 text-white px-6 py-3 rounded-lg hover:bg-indigo-600 font-semibold shadow-md transition"
                        >
                          ⛓️ Blockchain
                        </button>
                      </div>
                    </div>
                  </div>
                )}
              </div>
            )}

            {/* History Module */}
            {activeModule === 'history' && (
              <div>
                <h2 className="text-4xl font-bold mb-8 text-gray-800 flex items-center gap-3">
                  📜 Verification History
                </h2>
                
                <div className="mb-6 flex gap-4">
                  <select
                    value={filterStatus}
                    onChange={(e) => setFilterStatus(e.target.value)}
                    className="px-4 py-2 border-2 border-gray-300 rounded-lg focus:border-green-500 focus:outline-none"
                  >
                    <option value="">All Status</option>
                    <option value="valid">Valid</option>
                    <option value="invalid">Invalid</option>
                    <option value="tampered">Tampered</option>
                    <option value="revoked">Revoked</option>
                  </select>
                  <button
                    onClick={loadHistory}
                    className="bg-green-600 text-white px-6 py-2 rounded-lg hover:bg-green-700 font-semibold"
                  >
                    🔄 Refresh
                  </button>
                </div>
                
                <div className="overflow-x-auto rounded-xl border-2 border-gray-200">
                  <table className="w-full">
                    <thead className="bg-gradient-to-r from-gray-100 to-gray-200">
                      <tr>
                        <th className="p-4 text-left font-bold text-gray-700">Verification ID</th>
                        <th className="p-4 text-left font-bold text-gray-700">Certificate Hash</th>
                        <th className="p-4 text-center font-bold text-gray-700">Result</th>
                        <th className="p-4 text-center font-bold text-gray-700">Confidence</th>
                        <th className="p-4 text-left font-bold text-gray-700">Timestamp</th>
                      </tr>
                    </thead>
                    <tbody>
                      {history.map((h, idx) => (
                        <tr key={h.verification_id} className={`border-b hover:bg-gray-50 transition ${idx % 2 === 0 ? 'bg-white' : 'bg-gray-50'}`}>
                          <td className="p-4 font-mono text-xs text-gray-600">{h.verification_id.slice(0, 12)}...</td>
                          <td className="p-4 font-mono text-xs text-gray-600">{h.certificate_hash}</td>
                          <td className="p-4 text-center">
                            <span className={`px-3 py-1 rounded-lg text-xs font-bold ${getStatusColor(h.verification_result)}`}>
                              {h.verification_result}
                            </span>
                          </td>
                          <td className="p-4 text-center font-semibold text-gray-700">{(h.confidence_score * 100).toFixed(1)}%</td>
                          <td className="p-4 text-sm text-gray-600">{new Date(h.timestamp).toLocaleString()}</td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              </div>
            )}

            {/* Feedback Module */}
            {activeModule === 'feedback' && (
              <div>
                <h2 className="text-4xl font-bold mb-8 text-gray-800 flex items-center gap-3">
                  💬 Submit Feedback
                </h2>
                
                <form onSubmit={submitFeedback} className="space-y-6 mb-10 bg-gradient-to-r from-blue-50 to-indigo-50 p-8 rounded-xl border-2 border-blue-200">
                  <div>
                    <label className="block font-bold mb-2 text-gray-700">Feedback Type</label>
                    <select name="type" className="w-full px-4 py-3 border-2 border-gray-300 rounded-lg focus:border-blue-500 focus:outline-none" required>
                      <option value="suspicious">🚨 Suspicious Certificate</option>
                      <option value="issue">⚠️ Verification Issue</option>
                      <option value="general">💡 General Feedback</option>
                    </select>
                  </div>

                  <div>
                    <label className="block font-bold mb-2 text-gray-700">Priority</label>
                    <select name="priority" className="w-full px-4 py-3 border-2 border-gray-300 rounded-lg focus:border-blue-500 focus:outline-none">
                      <option value="low">🟢 Low</option>
                      <option value="medium">🟡 Medium</option>
                      <option value="high">🔴 High</option>
                    </select>
                  </div>

                  <div>
                    <label className="block font-bold mb-2 text-gray-700">Message</label>
                    <textarea
                      name="message"
                      rows="5"
                      className="w-full px-4 py-3 border-2 border-gray-300 rounded-lg focus:border-blue-500 focus:outline-none"
                      placeholder="Describe your feedback in detail..."
                      required
                    ></textarea>
                  </div>

                  <button type="submit" className="w-full bg-gradient-to-r from-blue-600 to-indigo-600 text-white px-6 py-4 rounded-lg hover:from-blue-700 hover:to-indigo-700 font-bold text-lg shadow-lg transition">
                    📤 Submit Feedback
                  </button>
                </form>

                <h3 className="font-bold text-2xl mb-6 text-gray-800">📋 My Feedback</h3>
                <div className="space-y-4">
                  {feedbacks.map(fb => (
                    <div key={fb.id} className="bg-gradient-to-r from-gray-50 to-gray-100 p-6 rounded-xl border-2 border-gray-200 shadow-md">
                      <div className="flex justify-between items-start mb-3">
                        <div>
                          <p className="font-bold text-lg text-gray-800">{fb.feedback_type}</p>
                          <p className="text-gray-600 mt-2">{fb.message}</p>
                        </div>
                        <span className={`px-3 py-1 rounded-lg text-xs font-bold ${
                          fb.priority === 'high' ? 'bg-red-100 text-red-800' :
                          fb.priority === 'medium' ? 'bg-yellow-100 text-yellow-800' :
                          'bg-green-100 text-green-800'
                        }`}>
                          {fb.priority}
                        </span>
                      </div>
                      <p className="text-xs text-gray-500">{new Date(fb.timestamp).toLocaleString()}</p>
                    </div>
                  ))}
                </div>
              </div>
            )}

            {/* Chatbot Module */}
            {activeModule === 'chatbot' && (
              <div>
                <h2 className="text-4xl font-bold mb-8 text-gray-800 flex items-center gap-3">
                  🤖 AI Verification Assistant
                </h2>
                
                <div className="bg-gradient-to-br from-gray-50 to-gray-100 rounded-xl p-6 h-96 overflow-y-auto mb-6 border-2 border-gray-200 shadow-inner">
                  {chatMessages.length === 0 && (
                    <div className="text-center text-gray-400 mt-20">
                      <div className="text-6xl mb-4">🤖</div>
                      <p>Ask me anything about certificate verification!</p>
                    </div>
                  )}
                  {chatMessages.map((msg, idx) => (
                    <div key={idx} className={`mb-4 ${msg.role === 'user' ? 'text-right' : 'text-left'}`}>
                      <div className={`inline-block px-5 py-3 rounded-xl shadow-md max-w-md ${
                        msg.role === 'user' 
                          ? 'bg-gradient-to-r from-green-500 to-green-600 text-white' 
                          : 'bg-white text-gray-800 border-2 border-gray-200'
                      }`}>
                        {msg.content}
                      </div>
                    </div>
                  ))}
                </div>

                <div className="flex gap-3">
                  <input
                    type="text"
                    value={chatInput}
                    onChange={(e) => setChatInput(e.target.value)}
                    onKeyPress={(e) => e.key === 'Enter' && sendChatMessage()}
                    className="flex-1 px-5 py-3 border-2 border-gray-300 rounded-xl focus:border-green-500 focus:outline-none"
                    placeholder="Ask about certificate verification..."
                  />
                  <button
                    onClick={sendChatMessage}
                    className="bg-gradient-to-r from-green-600 to-green-700 text-white px-8 py-3 rounded-xl hover:from-green-700 hover:to-green-800 font-bold shadow-lg transition"
                  >
                    📤 Send
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

export default VerifierDashboardEnhanced;
