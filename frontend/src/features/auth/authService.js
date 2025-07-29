// frontend/src/features/auth/authService.js

import api from '../../services/api'; // Import the centralized Axios instance

const AUTH_BASE_URL = '/auth'; // Matches Flask blueprint prefix

const authService = {
  /**
   * Registers a new user.
   * Corresponds to POST /auth/signup
   * @param {object} userData - { username, email, password, confirm_password }
   * @returns {Promise<object>} Response data on success.
   */
  signup: async (userData) => {
    try {
      const response = await api.post(`${AUTH_BASE_URL}/signup`, userData);
      return response.data;
    } catch (error) {
      console.error('Signup failed:', error.response ? error.response.data : error.message);
      throw error; // Re-throw to be handled by caller
    }
  },

  /**
   * Logs in a user.
   * Corresponds to POST /auth/login
   * @param {object} credentials - { username, password }
   * @returns {Promise<object>} Response data on success.
   */
  login: async (credentials) => {
    try {
      const response = await api.post(`${AUTH_BASE_URL}/login`, credentials);
      return response.data;
    } catch (error) {
      console.error('Login failed:', error.response ? error.response.data : error.message);
      throw error;
    }
  },

  /**
   * Logs out the current user.
   * Corresponds to POST /auth/logout
   * @returns {Promise<object>} Response data on success.
   */
  logout: async () => {
    try {
      const response = await api.post(`${AUTH_BASE_URL}/logout`);
      return response.data;
    } catch (error) {
      console.error('Logout failed:', error.response ? error.response.data : error.message);
      throw error;
    }
  },

  /**
   * Checks the current user's authentication status.
   * Corresponds to GET /auth/status
   * @returns {Promise<object>} { is_authenticated: boolean, user?: object }
   */
  checkAuthStatus: async () => {
    try {
      const response = await api.get(`${AUTH_BASE_URL}/status`);
      return response.data;
    } catch (error) {
      // For status check, a 401 just means not authenticated, not necessarily an error to throw
      if (error.response && error.response.status === 401) {
        return { is_authenticated: false, user: null };
      }
      console.error('Error checking auth status:', error.response ? error.response.data : error.message);
      throw error;
    }
  },
};

export default authService;