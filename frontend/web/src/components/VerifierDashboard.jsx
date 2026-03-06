import React, { useState } from 'react';
import { useAuth } from '../contexts/AuthContext';

const VerifierDashboard = () => {
  const { user, token, logout } = useAuth();
  const [activeTab, setActiveTab] = useState('verify');
  const [verificationResult, setVerificationResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [chatMessage, setChatMessage] = useState('');
  const [chatResponse, setChatResponse] = useState('');
  const [isChatLoading, setIsChatLoading] = useState(false);
  const [feedback, setFeedback] = useState({ message: '', category: 'verification' });

  const handleFileUpload = async (e) => {
    const file = e.target.files[0];
    if (!file) return;

    setLoading(true);
    const formData = new FormData();
    formData.append('file', file);

    try {
      const response = await fetch('http://localhost:8000/verifier/verify', {
        method: 'POST',
        headers: { 'Authorization': `Bearer ${token}` },
        body: formData
      });
      
      const result = await response.json();
      setVerificationResult(result);
    } catch (error) {
      setVerificationResult({ error: 'Verification failed' });
    } finally {
      setLoading(false);
    }
  };

  const handleChatSubmit = async (e) => {
    e.preventDefault();
    if (!chatMessage.trim()) return;
    
    setIsChatLoading(true);
    try {
      const response = await fetch('http://localhost:8000/chatbot', {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ 
          message: chatMessage,
          user_role: 'verifier',
          user_id: user?.id || 'verifier'
        })
      });
      
      const result = await response.json();
      setChatResponse(result.response || result.text_visualization || 'Response received');
      setChatMessage('');
    } catch (error) {
      setChatResponse('Error processing query: ' + error.message);
    } finally {
      setIsChatLoading(false);
    }
  };

  const handleFeedbackSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await fetch(`http://localhost:8000/verifier/feedback?message=${encodeURIComponent(feedback.message)}&category=${feedback.category}`, {
        method: 'POST',
        headers: { 'Authorization': `Bearer ${token}` }
      });
      
      if (response.ok) {
        alert('Feedback submitted successfully');
        setFeedback({ message: '', category: 'verification' });
      }
    } catch (error) {
      alert('Error submitting feedback');
    }
  };

  const renderVerification = () => (
    <div className="space-y-6">
      <div>
        <h3 className="text-lg font-semibold mb-4">Certificate Verification</h3>
        
        <div className="border-2 border-dashed border-gray-300 rounded-lg p-6 text-center">
          <input
            type="file"
            accept=".pdf,.jpg,.png"
            onChange={handleFileUpload}
            className="block w-full text-sm text-gray-500 file:mr-4 file:py-2 file:px-4 file:rounded-full file:border-0 file:text-sm file:font-semibold file:bg-blue-50 file:text-blue-700 hover:file:bg-blue-100"
          />
          <p className="mt-2 text-sm text-gray-600">
            Upload a certificate file (PDF, JPG, PNG) to verify its authenticity
          </p>
        </div>
      </div>

      {loading && (
        <div className="text-center py-8">
          <div className="inline-block animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
          <p className="mt-2">Verifying certificate...</p>
        </div>
      )}

      {verificationResult && !loading && (
        <div className="bg-white border rounded-lg p-6">
          <div className="flex items-center mb-4">
            <div className={`w-4 h-4 rounded-full mr-3 ${
              verificationResult.result ? 'bg-green-500' : 'bg-red-500'
            }`}></div>
            <h4 className="text-lg font-semibold">
              {verificationResult.result ? 'Certificate Verified ✓' : 'Certificate Invalid ✗'}
            </h4>
          </div>

          <div className="space-y-3">
            <div>
              <span className="font-medium">Hash:</span>
              <p className="text-sm text-gray-600 font-mono">{verificationResult.hash}</p>
            </div>

            {verificationResult.explanation && (
              <div>
                <span className="font-medium">AI Explanation:</span>
                <p className="text-sm text-gray-700 mt-1">{verificationResult.explanation}</p>
              </div>
            )}

            {verificationResult.ai_validation && (
              <div>
                <span className="font-medium">AI Validation:</span>
                <div className="mt-2 bg-gray-50 p-3 rounded">
                  <p className="text-sm">
                    <span className="font-medium">Confidence:</span> {(verificationResult.ai_validation.confidence * 100).toFixed(1)}%
                  </p>
                  <p className="text-sm">
                    <span className="font-medium">Format Valid:</span> {verificationResult.ai_validation.format_valid ? 'Yes' : 'No'}
                  </p>
                  <p className="text-sm">
                    <span className="font-medium">Keywords Found:</span> {verificationResult.ai_validation.keywords_found ? 'Yes' : 'No'}
                  </p>
                  {verificationResult.ai_validation.validation_token && (
                    <p className="text-sm">
                      <span className="font-medium">Validation Token:</span> {verificationResult.ai_validation.validation_token}
                    </p>
                  )}
                </div>
              </div>
            )}

            {verificationResult.blockchain_data && (
              <div>
                <span className="font-medium">Blockchain Data:</span>
                <div className="mt-2 bg-gray-50 p-3 rounded">
                  <p className="text-sm">
                    <span className="font-medium">Issuer:</span> {verificationResult.blockchain_data.issuer_id}
                  </p>
                  <p className="text-sm">
                    <span className="font-medium">Registered:</span> {new Date(verificationResult.blockchain_data.timestamp).toLocaleString()}
                  </p>
                </div>
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  );

  const renderChatbot = () => (
    <div className="space-y-4">
      <h3 className="text-lg font-semibold">AI Assistant</h3>
      <p className="text-sm text-gray-600">
        Ask questions about blockchain records, certificate validity, or verification processes.
      </p>
      
      <form onSubmit={handleChatSubmit} className="space-y-3">
        <textarea
          value={chatMessage}
          onChange={(e) => setChatMessage(e.target.value)}
          placeholder="Ask about certificate verification, blockchain records, or system processes..."
          className="w-full p-3 border rounded-lg resize-none"
          rows="3"
          disabled={isChatLoading}
        />
        <button
          type="submit"
          disabled={isChatLoading || !chatMessage.trim()}
          className="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700 disabled:bg-gray-400 disabled:cursor-not-allowed flex items-center space-x-2"
        >
          {isChatLoading ? (
            <>
              <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white"></div>
              <span>Processing...</span>
            </>
          ) : (
            <span>Ask AI</span>
          )}
        </button>
      </form>

      {isChatLoading && (
        <div className="bg-blue-50 p-4 rounded-lg border border-blue-200">
          <div className="flex items-center space-x-3">
            <div className="flex space-x-1">
              <div className="w-2 h-2 bg-blue-500 rounded-full animate-bounce"></div>
              <div className="w-2 h-2 bg-blue-500 rounded-full animate-bounce" style={{animationDelay: '0.1s'}}></div>
              <div className="w-2 h-2 bg-blue-500 rounded-full animate-bounce" style={{animationDelay: '0.2s'}}></div>
            </div>
            <span className="text-blue-700 font-medium">🤖 AI is analyzing your question...</span>
          </div>
        </div>
      )}

      {chatResponse && !isChatLoading && (
        <div className="bg-blue-50 p-4 rounded-lg border border-blue-200">
          <p className="font-medium text-blue-800 mb-2">🤖 AI Response:</p>
          <div className="text-blue-700 whitespace-pre-wrap">{chatResponse}</div>
        </div>
      )}

      <div className="mt-6 bg-gray-50 p-4 rounded-lg">
        <h4 className="font-medium mb-2">Sample Questions:</h4>
        <ul className="text-sm text-gray-600 space-y-1">
          <li>• How many certificates are registered on the blockchain?</li>
          <li>• What happens when a certificate is invalid?</li>
          <li>• How does the verification process work?</li>
          <li>• What is blockchain hash verification?</li>
        </ul>
      </div>
    </div>
  );

  const renderFeedback = () => (
    <div className="space-y-4">
      <h3 className="text-lg font-semibold">Submit Feedback</h3>
      <p className="text-sm text-gray-600">
        Share your experience with the verification process or report any issues.
      </p>
      
      <form onSubmit={handleFeedbackSubmit} className="space-y-4">
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Category
          </label>
          <select
            value={feedback.category}
            onChange={(e) => setFeedback(prev => ({ ...prev, category: e.target.value }))}
            className="w-full px-3 py-2 border border-gray-300 rounded-md"
          >
            <option value="verification">Verification Process</option>
            <option value="certificate_issues">Certificate Issues</option>
            <option value="system_experience">System Experience</option>
            <option value="feature_request">Feature Request</option>
            <option value="bug_report">Bug Report</option>
          </select>
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Message
          </label>
          <textarea
            value={feedback.message}
            onChange={(e) => setFeedback(prev => ({ ...prev, message: e.target.value }))}
            placeholder="Describe your feedback in detail..."
            className="w-full p-3 border rounded-lg resize-none"
            rows="4"
            required
          />
        </div>

        <button
          type="submit"
          className="px-4 py-2 bg-green-600 text-white rounded hover:bg-green-700"
        >
          Submit Feedback
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
              <h1 className="text-xl font-semibold">Verifier Dashboard</h1>
            </div>
            <div className="flex items-center space-x-4">
              <span className="text-sm text-gray-600">Welcome, {user?.id}</span>
              <button
                onClick={logout}
                className="px-3 py-1 bg-red-500 text-white rounded hover:bg-red-600"
              >
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
                { key: 'verify', label: 'Verify Certificate' },
                { key: 'chatbot', label: 'AI Assistant' },
                { key: 'feedback', label: 'Submit Feedback' }
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
              {activeTab === 'verify' && renderVerification()}
              {activeTab === 'chatbot' && renderChatbot()}
              {activeTab === 'feedback' && renderFeedback()}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default VerifierDashboard;