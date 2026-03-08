import React, { useState, useEffect } from 'react';
import axios from 'axios';
import Layout from './Layout';
import { StatCard, InfoCard, Button, Badge } from './UIComponents';

const API_URL = 'http://localhost:8000';

const VerifierDashboard = () => {
  const [activeModule, setActiveModule] = useState('dashboard');
  const [dashboardStats, setDashboardStats] = useState(null);
  const [verificationResult, setVerificationResult] = useState(null);
  const [history, setHistory] = useState([]);
  const [feedbacks, setFeedbacks] = useState([]);
  const [chatMessages, setChatMessages] = useState([
    { role: 'bot', content: `Hello! I'm your verification assistant. I can help you with:
• Your verification statistics
• Verification history
• Certificate verification process
• System information

What would you like to know?` }
  ]);
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
    setChatInput('');

    try {
      const res = await axios.get(
        `${API_URL}/verifier/ai-query`,
        { 
          params: { query: chatInput },
          headers 
        }
      );
      const botMessage = { role: 'bot', content: res.data.response };
      setChatMessages([...chatMessages, userMessage, botMessage]);
    } catch (err) {
      console.error('Chat error:', err);
      const errorMessage = { role: 'bot', content: 'Sorry, I encountered an error. Please try again.' };
      setChatMessages([...chatMessages, userMessage, errorMessage]);
    }
  };

  const handleLogout = () => {
    localStorage.removeItem('verifier_token');
    window.location.href = '/';
  };

  const navigationItems = [
    { id: 'dashboard', label: 'Dashboard' },
    { id: 'verify', label: 'Verify Certificate' },
    { id: 'history', label: 'History' },
    { id: 'feedback', label: 'Feedback' },
    { id: 'chatbot', label: 'Chatbot' }
  ];

  return (
    <>
      <Layout
        title="CertiSense Verifier"
        subtitle="Certificate Verification Platform"
        userRole="Verifier"
        onLogout={handleLogout}
        navigationItems={navigationItems}
        activeModule={activeModule}
        onModuleChange={setActiveModule}
        themeColor="green"
      >
        <div className="space-y-6">
            {/* MODULE 1: Dashboard */}
            {activeModule === 'dashboard' && dashboardStats && (
              <div className="space-y-6">
                <div>
                  <h2 className="text-2xl font-bold text-secondary-800">Verifier Dashboard</h2>
                  <p className="text-secondary-600 mt-1">Your verification statistics and performance metrics</p>
                </div>
                
                <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                  <StatCard 
                    title="Total Verifications"
                    value={dashboardStats.statistics.total_verifications}
                    icon="fa-check-double"
                    color="green"
                  />
                  <StatCard 
                    title="Valid Certificates"
                    value={dashboardStats.statistics.valid_certificates}
                    icon="fa-certificate"
                    color="blue"
                  />
                  <StatCard 
                    title="Success Rate"
                    value={`${dashboardStats.success_rate.toFixed(1)}%`}
                    icon="fa-chart-line"
                    color="purple"
                  />
                </div>

                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
                  <InfoCard title="Invalid Certificates" className="border-t-4 border-t-red-500">
                    <div className="flex items-center justify-between">
                      <div>
                        <p className="text-3xl font-bold text-red-600">{dashboardStats.statistics.invalid_certificates}</p>
                        <p className="text-sm text-secondary-600 mt-2">Failed verification</p>
                      </div>
                      <i className="fas fa-times-circle text-4xl text-red-300"></i>
                    </div>
                  </InfoCard>
                  
                  <InfoCard title="Tampered Certificates" className="border-t-4 border-t-orange-500">
                    <div className="flex items-center justify-between">
                      <div>
                        <p className="text-3xl font-bold text-orange-600">{dashboardStats.statistics.tampered_certificates}</p>
                        <p className="text-sm text-secondary-600 mt-2">Detected alterations</p>
                      </div>
                      <i className="fas fa-exclamation-triangle text-4xl text-orange-300"></i>
                    </div>
                  </InfoCard>
                </div>
              </div>
            )}

            {/* MODULE 2: Verify Certificate */}
            {activeModule === 'verify' && (
              <div className="space-y-6">
                <div>
                  <h2 className="text-2xl font-bold text-secondary-800">Verify Certificate</h2>
                  <p className="text-secondary-600 mt-1">Upload a certificate to verify its authenticity</p>
                </div>
                
                <InfoCard>
                  <form onSubmit={handleVerifyCertificate} className="space-y-6">
                    <div className="border-2 border-dashed border-secondary-300 rounded-lg p-8 text-center">
                      <i className="fas fa-cloud-upload-alt text-5xl text-secondary-400 mb-4"></i>
                      <input
                        type="file"
                        name="certificate"
                        accept=".pdf,.jpg,.jpeg,.png"
                        className="block w-full text-sm text-secondary-500 file:mr-4 file:py-2 file:px-4 file:rounded-lg file:border-0 file:text-sm file:font-semibold file:bg-green-50 file:text-green-700 hover:file:bg-green-100"
                        required
                      />
                      <p className="mt-2 text-sm text-secondary-600">Upload certificate (PDF, JPG, PNG)</p>
                    </div>

                    <Button
                      type="submit"
                      variant="success"
                      size="lg"
                      disabled={loading}
                      icon={loading ? 'fa-spinner fa-spin' : 'fa-check-circle'}
                      className="w-full"
                    >
                      {loading ? 'Verifying...' : 'Verify Certificate'}
                    </Button>
                  </form>
                </InfoCard>

                {verificationResult && (
                  <InfoCard title="Verification Result" icon="fa-clipboard-check">
                    <div className="space-y-4">
                      <div className="flex items-center gap-3">
                        <strong>Status:</strong>
                        <Badge variant={verificationResult.status === 'valid' ? 'success' : 'danger'}>
                          {verificationResult.status === 'valid' ? '✅ VALID CERTIFICATE' : '❌ INVALID CERTIFICATE'}
                        </Badge>
                      </div>
                      
                      {verificationResult.status === 'valid' && (
                        <div className="bg-green-50 p-4 rounded-lg border border-green-200">
                          <h4 className="font-semibold mb-3 text-green-800">Certificate Details</h4>
                          <div className="grid grid-cols-1 md:grid-cols-2 gap-3 text-sm">
                            <div>
                              <p className="text-secondary-600">Certificate ID:</p>
                              <p className="font-mono font-semibold">{verificationResult.certificate_id}</p>
                            </div>
                            <div>
                              <p className="text-secondary-600">Certificate Name:</p>
                              <p className="font-semibold">{verificationResult.certificate_name}</p>
                            </div>
                            <div>
                              <p className="text-secondary-600">Student Name:</p>
                              <p className="font-semibold">{verificationResult.student_name}</p>
                            </div>
                            <div>
                              <p className="text-secondary-600">Student ID:</p>
                              <p className="font-mono">{verificationResult.student_id}</p>
                            </div>
                            <div>
                              <p className="text-secondary-600">Institute:</p>
                              <p className="font-semibold">{verificationResult.institute_name}</p>
                            </div>
                            <div>
                              <p className="text-secondary-600">Institute ID:</p>
                              <p className="font-mono">{verificationResult.institute_id}</p>
                            </div>
                            <div>
                              <p className="text-secondary-600">Issue Date:</p>
                              <p>{verificationResult.issue_date ? new Date(verificationResult.issue_date).toLocaleDateString() : 'N/A'}</p>
                            </div>
                            <div>
                              <p className="text-secondary-600">Verification Count:</p>
                              <p className="font-semibold">{verificationResult.verification_count}</p>
                            </div>
                          </div>
                        </div>
                      )}
                      
                      <div className="bg-blue-50 p-3 rounded">
                        <p><strong>Certificate Hash:</strong></p>
                        <p className="font-mono text-xs break-all">{verificationResult.certificate_hash}</p>
                      </div>
                      
                      <div className="flex items-center gap-2">
                        <strong>Confidence Score:</strong>
                        <Badge variant="info">{(verificationResult.confidence_score * 100).toFixed(1)}%</Badge>
                      </div>
                      
                      <div className="flex items-center gap-2">
                        <strong>Blockchain Verified:</strong>
                        <Badge variant={verificationResult.blockchain_verified ? 'success' : 'danger'}>
                          {verificationResult.blockchain_verified ? '✅ Yes' : '❌ No'}
                        </Badge>
                      </div>
                      
                      {verificationResult.explanation && (
                        <div className="bg-yellow-50 p-3 rounded border border-yellow-200">
                          <p className="font-semibold mb-1">Explanation:</p>
                          <p className="text-sm">{verificationResult.explanation}</p>
                        </div>
                      )}
                      
                      {verificationResult.message && (
                        <div className={`p-3 rounded ${
                          verificationResult.status === 'valid' ? 'bg-green-50 border border-green-200' : 'bg-red-50 border border-red-200'
                        }`}>
                          <p className="text-sm">{verificationResult.message}</p>
                        </div>
                      )}
                    </div>
                  </InfoCard>
                )}
              </div>
            )}

            {/* MODULE 3: Verification History */}
            {activeModule === 'history' && (
              <div className="space-y-6">
                <div>
                  <h2 className="text-2xl font-bold text-secondary-800">Verification History</h2>
                  <p className="text-secondary-600 mt-1">View all your past verification activities</p>
                </div>
                
                <InfoCard>
                  <div className="table-container">
                    <table>
                      <thead>
                        <tr>
                          <th>Verification ID</th>
                          <th>Certificate Hash</th>
                          <th className="text-center">Result</th>
                          <th className="text-center">Confidence</th>
                          <th>Timestamp</th>
                        </tr>
                      </thead>
                      <tbody>
                        {history.map(h => (
                          <tr key={h.verification_id}>
                            <td className="font-mono text-xs">{h.verification_id.slice(0, 12)}...</td>
                            <td className="font-mono text-xs">{h.certificate_hash}</td>
                            <td className="text-center">
                              <Badge variant={h.verification_result === 'valid' ? 'success' : h.verification_result === 'invalid' ? 'danger' : 'warning'}>
                                {h.verification_result}
                              </Badge>
                            </td>
                            <td className="text-center">
                              <Badge variant="info">{(h.confidence_score * 100).toFixed(1)}%</Badge>
                            </td>
                            <td className="text-sm">
                              {new Date(h.timestamp).toLocaleString()}
                            </td>
                          </tr>
                        ))}
                      </tbody>
                    </table>
                  </div>
                </InfoCard>
              </div>
            )}

            {/* MODULE 4: Submit Feedback */}
            {activeModule === 'feedback' && (
              <div className="space-y-6">
                <div>
                  <h2 className="text-2xl font-bold text-secondary-800">Submit Feedback</h2>
                  <p className="text-secondary-600 mt-1">Share your feedback or report issues</p>
                </div>
                
                <InfoCard title="New Feedback">
                  <form onSubmit={submitFeedback} className="space-y-4">
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                      <div>
                        <label className="block font-medium mb-2">Feedback Type</label>
                        <select name="type" className="w-full" required>
                          <option value="suspicious">Suspicious Certificate</option>
                          <option value="issue">Verification Issue</option>
                          <option value="general">General Feedback</option>
                        </select>
                      </div>

                      <div>
                        <label className="block font-medium mb-2">Priority</label>
                        <select name="priority" className="w-full">
                          <option value="low">Low</option>
                          <option value="medium">Medium</option>
                          <option value="high">High</option>
                        </select>
                      </div>
                    </div>

                    <div>
                      <label className="block font-medium mb-2">Message</label>
                      <textarea
                        name="message"
                        rows="4"
                        className="w-full"
                        placeholder="Describe your feedback..."
                        required
                      ></textarea>
                    </div>

                    <Button type="submit" variant="success" icon="fa-paper-plane">
                      Submit Feedback
                    </Button>
                  </form>
                </InfoCard>

                <InfoCard title="My Feedback">
                  <div className="space-y-3">
                    {feedbacks.map(fb => (
                      <div key={fb.id} className="border rounded-lg p-4 hover:bg-secondary-50">
                        <div className="flex justify-between items-start">
                          <div className="flex-1">
                            <div className="flex items-center gap-2 mb-2">
                              <Badge variant="info">{fb.feedback_type}</Badge>
                              <Badge variant={fb.priority === 'high' ? 'danger' : fb.priority === 'medium' ? 'warning' : 'success'}>
                                {fb.priority}
                              </Badge>
                            </div>
                            <p className="text-sm text-secondary-700">{fb.message}</p>
                          </div>
                        </div>
                        <p className="text-xs text-secondary-500 mt-2">{new Date(fb.timestamp).toLocaleString()}</p>
                      </div>
                    ))}
                  </div>
                </InfoCard>
              </div>
            )}

            {/* MODULE 5: Verification Assistant Chatbot */}
            {activeModule === 'chatbot' && (
              <div className="space-y-6">
                <div>
                  <h2 className="text-2xl font-bold text-secondary-800">🤖 Verification Assistant</h2>
                  <p className="text-secondary-600 mt-1">Ask me about your verification statistics, certificates, and activity</p>
                </div>
                
                <InfoCard>
                  <div className="bg-secondary-50 rounded-lg p-4 h-[500px] overflow-y-auto mb-4 border border-secondary-200">
                    {chatMessages.map((msg, idx) => (
                      <div key={idx} className={`mb-4 ${msg.role === 'user' ? 'text-right' : 'text-left'}`}>
                        <div className={`inline-block max-w-[80%] px-4 py-3 rounded-lg shadow-sm ${
                          msg.role === 'user' 
                            ? 'bg-green-500 text-white rounded-br-none' 
                            : 'bg-white text-secondary-800 border border-secondary-200 rounded-bl-none'
                        }`}>
                          <pre className="whitespace-pre-wrap font-sans text-sm">{msg.content}</pre>
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
                      className="flex-1"
                      placeholder="Ask: 'Show my statistics' or 'How many valid certificates?'"
                    />
                    <Button onClick={sendChatMessage} variant="success" icon="fa-paper-plane">
                      Send
                    </Button>
                  </div>
                  
                  <div className="mt-4 bg-blue-50 p-4 rounded-lg border border-blue-200">
                    <p className="text-sm text-blue-800 font-semibold mb-2">💡 Try asking:</p>
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-2 text-sm">
                      <button onClick={() => setChatInput('Show my statistics')} className="text-left text-blue-600 hover:underline">• Show my statistics</button>
                      <button onClick={() => setChatInput('How many valid certificates?')} className="text-left text-blue-600 hover:underline">• How many valid certificates?</button>
                      <button onClick={() => setChatInput('Recent activity')} className="text-left text-blue-600 hover:underline">• Recent activity</button>
                      <button onClick={() => setChatInput('Show certificate hashes')} className="text-left text-blue-600 hover:underline">• Show certificate hashes</button>
                    </div>
                  </div>
                </InfoCard>
              </div>
            )}
        </div>
      </Layout>

    </>
  );
};

export default VerifierDashboard;
