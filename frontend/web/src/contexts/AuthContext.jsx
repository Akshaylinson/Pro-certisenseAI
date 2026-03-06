import React, { createContext, useContext, useState, useEffect } from 'react';

const AuthContext = createContext();

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};

// Helper functions for role-specific token management
const getTokenKey = (role) => `${role}_token`;

const getStoredToken = (role) => {
  if (!role) return null;
  return localStorage.getItem(getTokenKey(role));
};

const setStoredToken = (role, token) => {
  localStorage.setItem(getTokenKey(role), token);
};

const removeStoredToken = (role) => {
  localStorage.removeItem(getTokenKey(role));
};

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [token, setToken] = useState(null);

  // Initialize from stored tokens on mount
  useEffect(() => {
    const roles = ['admin', 'institute', 'student', 'verifier'];
    for (const role of roles) {
      const storedToken = getStoredToken(role);
      if (storedToken) {
        try {
          const payload = JSON.parse(atob(storedToken.split('.')[1]));
          if (payload.role === role) {
            setToken(storedToken);
            setUser({ id: payload.user_id, role: payload.role });
            break;
          }
        } catch (error) {
          removeStoredToken(role);
        }
      }
    }
  }, []);

  const login = (accessToken, role) => {
    setStoredToken(role, accessToken);
    setToken(accessToken);
    const payload = JSON.parse(atob(accessToken.split('.')[1]));
    setUser({ id: payload.user_id, role });
  };

  const logout = () => {
    if (user?.role) {
      removeStoredToken(user.role);
    }
    setToken(null);
    setUser(null);
  };

  const value = {
    user,
    token,
    login,
    logout,
    isAuthenticated: !!user,
    isAdmin: user?.role === 'admin',
    isInstitute: user?.role === 'institute',
    isStudent: user?.role === 'student',
    isVerifier: user?.role === 'verifier'
  };

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  );
};