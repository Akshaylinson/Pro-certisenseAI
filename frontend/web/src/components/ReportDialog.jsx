import React from 'react';
import API_URL from '../config/api';

const ReportDialog = ({ isOpen, onClose, reportData, reportType, loading }) => {
  if (!isOpen) return null;

  const getReportTitle = (type) => {
    const titles = {
      'institute': '📊 Institute Performance Report',
      'certificates': '📜 Certificate Analytics Report',
      'verifications': '✅ Verification Success Report',
      'system': '📈 System Activity Report'
    };
    return titles[type] || 'Report';
  };

  const formatMetricValue = (value) => {
    if (typeof value === 'number') {
      return value.toLocaleString();
    }
    return value;
  };

  const downloadChart = () => {
    if (reportData?.chart_url) {
      const link = document.createElement('a');
      link.href = `${API_URL}${reportData.chart_url}`;
      link.download = `${reportType}_report_${new Date().toISOString().split('T')[0]}.png`;
      link.click();
    }
  };

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
      <div className="bg-white rounded-lg shadow-xl max-w-4xl w-full max-h-[90vh] overflow-y-auto">
        {/* Header */}
        <div className="flex justify-between items-center p-6 border-b">
          <h2 className="text-2xl font-bold text-gray-800">
            {getReportTitle(reportType)}
          </h2>
          <button
            onClick={onClose}
            className="text-gray-500 hover:text-gray-700 text-2xl font-bold"
          >
            ×
          </button>
        </div>

        {/* Content */}
        <div className="p-6">
          {loading ? (
            <div className="text-center py-12">
              <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-500 mx-auto"></div>
              <p className="mt-4 text-gray-600">Generating AI-powered report...</p>
            </div>
          ) : reportData ? (
            <div className="space-y-6">
              {/* Section 1: Key Metrics */}
              <div>
                <h3 className="text-xl font-bold mb-4 text-gray-800">📊 Key Metrics</h3>
                <div className="grid grid-cols-2 md:grid-cols-3 gap-4">
                  {Object.entries(reportData.metrics || {}).map(([key, value]) => {
                    if (key === 'daily_activity_trend') return null;
                    return (
                      <div key={key} className="bg-gray-50 p-4 rounded-lg border">
                        <p className="text-sm text-gray-600 capitalize">
                          {key.replace(/_/g, ' ')}
                        </p>
                        <p className="text-2xl font-bold text-blue-600">
                          {formatMetricValue(value)}
                        </p>
                      </div>
                    );
                  })}
                </div>
              </div>

              {/* Section 2: AI Insights */}
              <div>
                <h3 className="text-xl font-bold mb-4 text-gray-800">🤖 AI Insights</h3>
                <div className="bg-blue-50 p-6 rounded-lg border border-blue-200">
                  <div className="whitespace-pre-line text-gray-700 leading-relaxed">
                    {reportData.ai_summary || 'AI analysis not available.'}
                  </div>
                </div>
              </div>

              {/* Section 3: Chart Display */}
              {reportData.chart_url && (
                <div>
                  <div className="flex justify-between items-center mb-4">
                    <h3 className="text-xl font-bold text-gray-800">📈 Visual Analysis</h3>
                    <button
                      onClick={downloadChart}
                      className="bg-green-500 text-white px-4 py-2 rounded-lg hover:bg-green-600 transition flex items-center gap-2"
                    >
                      📥 Download Chart
                    </button>
                  </div>
                  <div className="bg-white p-4 rounded-lg border shadow-sm">
                    <img
                      src={`${API_URL}${reportData.chart_url}`}
                      alt={`${reportType} report chart`}
                      className="w-full h-auto rounded-lg"
                      onError={(e) => {
                        e.target.style.display = 'none';
                        e.target.nextSibling.style.display = 'block';
                      }}
                    />
                    <div 
                      className="text-center py-8 text-gray-500 hidden"
                    >
                      Chart could not be loaded
                    </div>
                  </div>
                </div>
              )}

              {/* Section 4: Report Details */}
              <div className="bg-gray-50 p-4 rounded-lg border">
                <div className="flex justify-between items-center text-sm text-gray-600">
                  <span>Report generated: {new Date(reportData.generated_at).toLocaleString()}</span>
                  <span>Report type: {reportType.charAt(0).toUpperCase() + reportType.slice(1)}</span>
                </div>
              </div>
            </div>
          ) : (
            <div className="text-center py-12">
              <p className="text-gray-600">Failed to generate report. Please try again.</p>
            </div>
          )}
        </div>

        {/* Footer */}
        <div className="flex justify-end gap-3 p-6 border-t bg-gray-50">
          <button
            onClick={onClose}
            className="px-6 py-2 bg-gray-500 text-white rounded-lg hover:bg-gray-600 transition"
          >
            Close
          </button>
          {reportData && (
            <button
              onClick={downloadChart}
              className="px-6 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600 transition"
            >
              Download Report
            </button>
          )}
        </div>
      </div>
    </div>
  );
};

export default ReportDialog;