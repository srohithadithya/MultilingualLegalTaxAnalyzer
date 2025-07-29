// frontend/src/features/auth/AuthProvider.jsx

import React, { createContext, useContext, useState, useEffect } from 'react';
import PropTypes from 'prop-types';
import authService from './authService'; // Import authService for API calls
import LoadingSpinner from '../../components/LoadingSpinner/LoadingSpinner'; // Reusable spinner component

// Create the AuthContext
export const AuthContext = createContext(null);

/**
 * AuthProvider component that manages authentication state and provides it via context.
 * It also handles initial authentication status check on app load.
 */
export const AuthProvider = ({ children }) => {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [user, setUser] = useState(null); // Stores user data if authenticated
  const [loading, setLoading] = useState(true); // Tracks initial auth check loading

  // Effect to check auth status on component mount
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
        setLoading(false); // Authentication check is complete
      }
    };
    checkStatus();
  }, []);

  /**
   * Handles user login.
   * @param {object} credentials - { username, password }
   * @returns {Promise<boolean>} True if login successful, false otherwise.
   */
  const login = async (credentials) => {
    try {
      const response = await authService.login(credentials);
      setIsAuthenticated(true);
      setUser(response.user); // Assuming backend sends back user data on successful login
      return true;
    } catch (error) {
      console.error("Login failed:", error);
      setIsAuthenticated(false);
      setUser(null);
      throw error; // Re-throw to allow caller to handle UI errors
    }
  };

  /**
   * Handles user logout.
   */
  const logout = async () => {
    try {
      await authService.logout();
      setIsAuthenticated(false);
      setUser(null);
    } catch (error) {
      console.error("Logout failed:", error);
      // Even if logout API fails, clear local state for UX
      setIsAuthenticated(false);
      setUser(null);
      throw error;
    }
  };

  // Provide the auth state and functions via context
  const authContextValue = {
    isAuthenticated,
    user,
    loading,
    login,
    logout,
    signup: authService.signup, // Directly expose signup as it doesn't change local state instantly
  };

  if (loading) {
    // Show a global loading spinner while checking initial auth status
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

// Custom hook to consume the AuthContext
export const useAuth = () => {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};