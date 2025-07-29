// frontend/src/features/auth/components/SignupForm.jsx

import React, { useState } from 'react';
import PropTypes from 'prop-types';
import { useAuth } from '../hooks/useAuth'; // Import the custom auth hook
import Button from '../../../components/Button/Button'; // Reusable Button
import {
  isValidEmail,
  validatePasswordStrength,
  isNotEmpty,
} from '../../../utils/validationUtils'; // Import validation utilities
import styles from './AuthForms.module.scss'; // Shared styles for auth forms

/**
 * SignupForm component for new user registration.
 * Handles form state, submission, and displays validation/error messages.
 */
const SignupForm = ({ onSuccess, onSwitchToLogin }) => {
  const { signup } = useAuth(); // Get signup function from auth context
  const [username, setUsername] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError(''); // Clear previous errors
    setLoading(true);

    // --- Client-side validation ---
    if (!isNotEmpty(username) || !isNotEmpty(email) || !isNotEmpty(password) || !isNotEmpty(confirmPassword)) {
      setError('All fields are required.');
      setLoading(false);
      return;
    }
    if (!isValidEmail(email)) {
      setError('Please enter a valid email address.');
      setLoading(false);
      return;
    }
    const { isValid, message: passwordMessage } = validatePasswordStrength(password);
    if (!isValid) {
      setError(passwordMessage);
      setLoading(false);
      return;
    }
    if (password !== confirmPassword) {
      setError('Passwords do not match.');
      setLoading(false);
      return;
    }
    // --- End client-side validation ---

    try {
      const response = await signup({ username, email, password, confirm_password: confirmPassword });
      onSuccess(response.message || 'Registration successful! Please login.'); // Callback to parent
    } catch (err) {
      const errorMessage =
        err.response && err.response.data && err.response.data.message
          ? err.response.data.message
          : 'An unexpected error occurred during registration.';
      setError(errorMessage);
    } finally {
      setLoading(false);
    }
  };

  return (
    <form onSubmit={handleSubmit} className={styles.authForm}>
      <h2 className={styles.formTitle}>Sign Up</h2>
      {error && <p className={styles.errorMessage}>{error}</p>}

      <div className={styles.formGroup}>
        <label htmlFor="signup-username">Username</label>
        <input
          type="text"
          id="signup-username"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
          required
          autoComplete="username"
        />
      </div>

      <div className={styles.formGroup}>
        <label htmlFor="signup-email">Email</label>
        <input
          type="email"
          id="signup-email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          required
          autoComplete="email"
        />
      </div>

      <div className={styles.formGroup}>
        <label htmlFor="signup-password">Password</label>
        <input
          type="password"
          id="signup-password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          required
          autoComplete="new-password"
        />
      </div>

      <div className={styles.formGroup}>
        <label htmlFor="signup-confirm-password">Confirm Password</label>
        <input
          type="password"
          id="signup-confirm-password"
          value={confirmPassword}
          onChange={(e) => setConfirmPassword(e.target.value)}
          required
          autoComplete="new-password"
        />
      </div>

      <Button type="submit" isLoading={loading} disabled={loading} className={styles.submitButton}>
        {loading ? 'Signing Up...' : 'Sign Up'}
      </Button>

      <p className={styles.switchFormText}>
        Already have an account?{' '}
        <span className={styles.switchFormLink} onClick={onSwitchToLogin}>
          Login
        </span>
      </p>
    </form>
  );
};

SignupForm.propTypes = {
  onSuccess: PropTypes.func.isRequired,
  onSwitchToLogin: PropTypes.func.isRequired,
};

export default SignupForm;