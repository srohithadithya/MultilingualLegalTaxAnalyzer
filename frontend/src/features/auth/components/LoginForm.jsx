// frontend/src/features/auth/components/LoginForm.jsx

import React, { useState } from 'react';
import PropTypes from 'prop-types';
import { useAuth } from '../hooks/useAuth'; // Import the custom auth hook
import Button from '../../../components/Button/Button'; // Reusable Button
import styles from './AuthForms.module.scss'; // Shared styles for auth forms

/**
 * LoginForm component for user authentication.
 * Handles form state, submission, and displays error messages.
 */
const LoginForm = ({ onSuccess, onSwitchToSignup }) => {
  const { login } = useAuth(); // Get login function from auth context
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError(''); // Clear previous errors
    setLoading(true);

    if (!username || !password) {
      setError('Please enter both username and password.');
      setLoading(false);
      return;
    }

    try {
      const success = await login({ username, password });
      if (success) {
        onSuccess(); // Callback to parent (e.g., redirect to dashboard)
      } else {
        // This path is usually handled by the catch block
        setError('Login failed. Please check your credentials.');
      }
    } catch (err) {
      const errorMessage = err.response && err.response.data && err.response.data.message
                           ? err.response.data.message
                           : 'An unexpected error occurred during login.';
      setError(errorMessage);
    } finally {
      setLoading(false);
    }
  };

  return (
    <form onSubmit={handleSubmit} className={styles.authForm}>
      <h2 className={styles.formTitle}>Login</h2>
      {error && <p className={styles.errorMessage}>{error}</p>}

      <div className={styles.formGroup}>
        <label htmlFor="login-username">Username</label>
        <input
          type="text"
          id="login-username"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
          required
          autoComplete="username"
        />
      </div>

      <div className={styles.formGroup}>
        <label htmlFor="login-password">Password</label>
        <input
          type="password"
          id="login-password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          required
          autoComplete="current-password"
        />
      </div>

      <Button type="submit" isLoading={loading} disabled={loading} className={styles.submitButton}>
        {loading ? 'Logging In...' : 'Login'}
      </Button>

      <p className={styles.switchFormText}>
        Don't have an account?{' '}
        <span className={styles.switchFormLink} onClick={onSwitchToSignup}>
          Sign Up
        </span>
      </p>
    </form>
  );
};

LoginForm.propTypes = {
  onSuccess: PropTypes.func.isRequired,
  onSwitchToSignup: PropTypes.func.isRequired,
};

export default LoginForm;