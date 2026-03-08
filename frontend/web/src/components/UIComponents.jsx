import React from 'react';

export const StatCard = ({ title, value, icon, color = 'blue', description }) => {
  const colors = {
    blue: 'from-blue-500 to-blue-600',
    green: 'from-green-500 to-green-600',
    purple: 'from-purple-500 to-purple-600',
    yellow: 'from-yellow-500 to-yellow-600',
    red: 'from-red-500 to-red-600',
    indigo: 'from-indigo-500 to-indigo-600'
  };

  return (
    <div className={`bg-gradient-to-br ${colors[color]} text-white p-6 rounded-xl shadow-lg hover:shadow-xl transition-all duration-200 transform hover:-translate-y-1`}>
      <div className="flex items-start justify-between">
        <div className="flex-1">
          <h3 className="text-sm font-semibold opacity-90 mb-2">{title}</h3>
          <p className="text-4xl font-bold">{value}</p>
          {description && (
            <p className="text-xs mt-2 opacity-80">{description}</p>
          )}
        </div>
        {icon && (
          <div className="text-3xl opacity-80">
            <i className={`fas ${icon}`}></i>
          </div>
        )}
      </div>
    </div>
  );
};

export const InfoCard = ({ title, children, className = '', headerAction }) => {
  return (
    <div className={`bg-white rounded-xl shadow-md border border-secondary-200 p-6 ${className}`}>
      {(title || headerAction) && (
        <div className="flex items-center justify-between mb-4 pb-3 border-b border-secondary-100">
          {title && <h3 className="font-semibold text-lg text-secondary-800">{title}</h3>}
          {headerAction && <div>{headerAction}</div>}
        </div>
      )}
      <div>{children}</div>
    </div>
  );
};

export const Button = ({ 
  children, 
  variant = 'primary', 
  size = 'md', 
  onClick, 
  type = 'button',
  disabled = false,
  className = '',
  icon
}) => {
  const variants = {
    primary: 'bg-primary-600 hover:bg-primary-700 text-white shadow-md hover:shadow-lg',
    secondary: 'bg-secondary-100 hover:bg-secondary-200 text-secondary-700 border border-secondary-300',
    success: 'bg-green-600 hover:bg-green-700 text-white shadow-md',
    danger: 'bg-red-600 hover:bg-red-700 text-white shadow-md',
    warning: 'bg-yellow-500 hover:bg-yellow-600 text-white shadow-md'
  };

  const sizes = {
    sm: 'px-3 py-1.5 text-sm',
    md: 'px-4 py-2 text-base',
    lg: 'px-6 py-3 text-lg'
  };

  return (
    <button
      type={type}
      onClick={onClick}
      disabled={disabled}
      className={`
        ${variants[variant]} 
        ${sizes[size]} 
        rounded-lg font-medium 
        transition-all duration-200 
        flex items-center gap-2
        disabled:opacity-50 disabled:cursor-not-allowed
        ${!disabled && 'hover:-translate-y-0.5'}
        ${className}
      `}
    >
      {icon && <i className={`fas ${icon}`}></i>}
      {children}
    </button>
  );
};

export const Badge = ({ children, variant = 'info' }) => {
  const variants = {
    success: 'bg-green-100 text-green-800',
    danger: 'bg-red-100 text-red-800',
    warning: 'bg-yellow-100 text-yellow-800',
    info: 'bg-blue-100 text-blue-800',
    neutral: 'bg-gray-100 text-gray-800'
  };

  return (
    <span className={`px-3 py-1 rounded-full text-xs font-medium ${variants[variant]}`}>
      {children}
    </span>
  );
};
