// frontend/src/features/auth/hooks/useAuth.js

import { useContext } from 'react';
import { AuthContext } from '../AuthProvider'; // Import the AuthContext

/**
 * Custom hook to easily access authentication state and actions.
 * @returns {object} An object containing isAuthenticated, user, loading, login, logout, signup.
 */
export const useAuth = () => {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};

export default useAuth;