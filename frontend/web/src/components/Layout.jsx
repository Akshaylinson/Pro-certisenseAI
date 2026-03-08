import React, { useState } from 'react';

const Layout = ({ 
  children, 
  title, 
  subtitle, 
  userRole, 
  onLogout, 
  navigationItems, 
  activeModule, 
  onModuleChange,
  themeColor = 'blue'
}) => {
  const [sidebarOpen, setSidebarOpen] = useState(false);

  const themeColors = {
    blue: {
      bg: 'bg-blue-600',
      bgHover: 'hover:bg-blue-700',
      text: 'text-blue-600',
      light: 'bg-blue-50',
      border: 'border-blue-200'
    },
    green: {
      bg: 'bg-green-600',
      bgHover: 'hover:bg-green-700',
      text: 'text-green-600',
      light: 'bg-green-50',
      border: 'border-green-200'
    },
    purple: {
      bg: 'bg-purple-600',
      bgHover: 'hover:bg-purple-700',
      text: 'text-purple-600',
      light: 'bg-purple-50',
      border: 'border-purple-200'
    }
  };

  const theme = themeColors[themeColor] || themeColors.blue;

  const getIconForModule = (moduleId) => {
    const icons = {
      dashboard: 'fa-chart-line',
      institutes: 'fa-building-columns',
      certificates: 'fa-certificate',
      students: 'fa-user-graduate',
      verifiers: 'fa-user-shield',
      verifications: 'fa-check-double',
      reports: 'fa-file-waveform',
      feedback: 'fa-comments',
      profile: 'fa-user',
      history: 'fa-clock-rotate-left',
      verify: 'fa-magnifying-glass',
      chatbot: 'fa-robot'
    };
    return icons[moduleId] || 'fa-circle';
  };

  return (
    <div className="min-h-screen bg-secondary-50">
      {/* Top Navigation Header */}
      <header className="bg-white shadow-sm border-b border-secondary-200 sticky top-0 z-30">
        <div className="max-w-[1920px] mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            {/* Left side - Logo and Title */}
            <div className="flex items-center gap-4">
              <button
                onClick={() => setSidebarOpen(!sidebarOpen)}
                className="lg:hidden p-2 rounded-lg hover:bg-secondary-100"
              >
                <i className="fas fa-bars text-lg"></i>
              </button>
              
              <div>
                <h1 className="text-xl font-bold text-secondary-900 flex items-center gap-2">
                  <i className={`fas fa-shield-halved ${theme.text}`}></i>
                  {title}
                </h1>
                {subtitle && (
                  <p className="text-xs text-secondary-500">{subtitle}</p>
                )}
              </div>
            </div>

            {/* Right side - User Info and Logout */}
            <div className="flex items-center gap-4">
              <div className="hidden md:flex items-center gap-2 px-3 py-1.5 bg-secondary-50 rounded-lg border border-secondary-200">
                <i className={`fas fa-user-circle ${theme.text}`}></i>
                <span className="text-sm font-medium text-secondary-700">{userRole}</span>
              </div>
              
              <button
                onClick={onLogout}
                className={`${theme.bg} ${theme.bgHover} text-white px-4 py-2 rounded-lg font-medium transition-all duration-200 flex items-center gap-2 hover:shadow-md`}
              >
                <i className="fas fa-sign-out-alt"></i>
                <span className="hidden sm:inline">Logout</span>
              </button>
            </div>
          </div>
        </div>
      </header>

      <div className="max-w-[1920px] mx-auto px-4 sm:px-6 lg:px-8 py-6">
        <div className="flex gap-6">
          {/* Sidebar Navigation */}
          <aside className={`
            w-64 bg-white rounded-lg shadow-lg border border-secondary-200 
            ${sidebarOpen ? 'block' : 'hidden'} lg:block
            sidebar flex-shrink-0
          `}>
            <nav className="p-4 space-y-1">
              {navigationItems.map((item) => (
                <button
                  key={item.id}
                  onClick={() => {
                    onModuleChange(item.id);
                    setSidebarOpen(false);
                  }}
                  className={`
                    w-full flex items-center gap-3 px-4 py-3 rounded-lg 
                    transition-all duration-200 group
                    ${activeModule === item.id 
                      ? `${theme.light} ${theme.text} shadow-md border-l-4 ${theme.border}` 
                      : 'text-secondary-600 hover:bg-secondary-50 hover:text-secondary-900'
                    }
                  `}
                >
                  <i className={`fas ${getIconForModule(item.id)} text-lg w-5`}></i>
                  <span className="font-medium">{item.label}</span>
                  {item.badge && (
                    <span className="ml-auto bg-red-500 text-white text-xs px-2 py-0.5 rounded-full">
                      {item.badge}
                    </span>
                  )}
                </button>
              ))}
            </nav>
          </aside>

          {/* Overlay for mobile */}
          {sidebarOpen && (
            <div
              className="fixed inset-0 bg-black bg-opacity-50 z-20 lg:hidden"
              onClick={() => setSidebarOpen(false)}
            ></div>
          )}

          {/* Main Content Area */}
          <main className="flex-1 bg-white rounded-lg shadow-lg border border-secondary-200 p-6 overflow-auto">
            {children}
          </main>
        </div>
      </div>
    </div>
  );
};

export default Layout;
