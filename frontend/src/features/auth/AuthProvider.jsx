// frontend/src/features/auth/AuthProvider.jsx

import React, { createContext, useContext, useState, useEffect } from 'react';
import PropTypes from 'prop-types';
import authService from './authService';
import LoadingSpinner from '../../components/LoadingSpinner/LoadingSpinner';

export const AuthContext = createContext(null);

export const AuthProvider = ({ children }) => {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const checkStatus = async () => {
      try {
        const data = await authService.checkAuthStatus();
        setIsAuthenticated(data.is_authenticated);
        setUser(data.user || null);
      } catch (error) {
        console.error("Failed to check auth status on load:", error);
        setIsAuthenticated(false);
        setUser(null);
      } finally {
        setLoading(false);
      }
    };
    checkStatus();
  }, []);

  const login = async (credentials) => {
    try {
      const response = await authService.login(credentials);
      setIsAuthenticated(true);
      setUser(response.user);
      return true;
    } catch (error) {
      console.error("Login failed:", error);
      setIsAuthenticated(false);
      setUser(null);
      throw error;
    }
  };

  const logout = async () => {
    try {
      await authService.logout();
      setIsAuthenticated(false);
      setUser(null);
    } catch (error) {
      console.error("Logout failed:", error);
      setIsAuthenticated(false);
      setUser(null);
      throw error;
    }
  };

  const authContextValue = {
    isAuthenticated,
    user,
    loading,
    login,
    logout,
    signup: authService.signup,
  };

  if (loading) {
    return (
      <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', minHeight: '100vh' }}>
        <LoadingSpinner size="lg" />
      </div>
    );
  }

  return (
    <AuthContext.Provider value={authContextValue}>
      {children}
    </AuthContext.Provider>
  );
};

AuthProvider.propTypes = {
  children: PropTypes.node.isRequired,
};

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};
