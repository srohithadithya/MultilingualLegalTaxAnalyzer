// frontend/src/layouts/AuthLayout.jsx

import React from 'react';
import PropTypes from 'prop-types';
import { Outlet } from 'react-router-dom';
import styles from './AuthLayout.module.scss'; // Module SCSS for this layout
import analyzerLogo from '../assets/images/analyzer-logo.svg'; // Your logo asset

/**
 * AuthLayout component for public pages (e.g., login, signup).
 * Provides a simple, centered layout for authentication forms.
 */
const AuthLayout = () => {
  return (
    <div className={styles.authLayout}>
      <div className={styles.authCard}>
        <img src={analyzerLogo} alt="Analyzer Logo" className={styles.logo} />
        <h1 className={styles.title}>Welcome to Tax Analyzer</h1>
        <p className={styles.subtitle}>Your multi-lingual legal tax assistant</p>
        <Outlet /> {/* Renders the current authentication route's component (LoginForm or SignupForm) */}
      </div>
      <footer className={styles.footer}>
        <p>&copy; {new Date().getFullYear()} Multi-Lingual Tax Analyzer</p>
      </footer>
    </div>
  );
};

AuthLayout.propTypes = {
  // Children are implicitly handled by Outlet
};

export default AuthLayout;