// frontend/src/layouts/MainLayout.jsx

import React from 'react';
import PropTypes from 'prop-types';
import { Outlet, Link, useNavigate } from 'react-router-dom';
import { useAuth } from '~features/auth/hooks/useAuth.jsx'; // Updated import path and .jsx
import { useMessage } from '~store/messageStore.jsx'; // Updated import path and .jsx
import Button from '~components/Button/Button'; // Updated import path using alias
import LoadingSpinner from '~components/LoadingSpinner/LoadingSpinner'; // Updated import path using alias

// Import SVG as a React Component using '?react' suffix for vite-plugin-svgr
import AnalyzerLogo from '~assets/images/analyzer-logo.svg?react'; // Updated import path and ?react

import styles from './MainLayout.module.scss';

/**
 * MainLayout component for authenticated users.
 * Includes a header, navigation, and renders child routes via <Outlet />.
 * Also displays global messages (toasts/alerts).
 */
const MainLayout = () => {
  const { user, logout, isAuthenticated } = useAuth();
  const { messages, removeMessage } = useMessage();
  const navigate = useNavigate();

  const handleLogout = async () => {
    try {
      await logout();
      navigate('/auth/login');
    } catch (error) {
      console.error('Logout error:', error);
    }
  };

  if (!isAuthenticated) {
    return (
      <div className={styles.unauthenticatedRedirect}>
        <LoadingSpinner size="lg" />
        <p>Redirecting to login...</p>
      </div>
    );
  }

  return (
    <div className={styles.mainLayout}>
      <header className={styles.header}>
        <div className={styles.headerContent}>
          <Link to="/dashboard" className={styles.logoLink}>
            {/* Use the SVG as a React component */}
            <AnalyzerLogo className={styles.logo} /> {/* Apply custom class for styling */}
            <span className={styles.appName}>Tax Analyzer</span>
          </Link>
          <nav className={styles.navbarNav}>
            <ul>
              <li><Link to="/dashboard">Dashboard</Link></li>
            </ul>
          </nav>
          <div className={styles.userControls}>
            <span className={styles.welcomeText}>Welcome, {user?.username || 'User'}!</span>
            <Button onClick={handleLogout} variant="outline" size="sm">
              Logout
            </Button>
          </div>
        </div>
      </header>

      <main className={styles.content}>
        <Outlet />
      </main>

      <footer className={styles.footer}>
        <p>&copy; {new Date().getFullYear()} Multi-Lingual Tax Analyzer. All rights reserved.</p>
        <p>Built with ❤️ by Your Team.</p>
      </footer>

      <div className={styles.messageContainer}>
        {messages.map((msg) => (
          <div key={msg.id} className={`${styles.messageItem} ${styles[msg.type]}`} onClick={() => removeMessage(msg.id)}>
            <p>{msg.text}</p>
            <button className={styles.closeButton}>&times;</button>
          </div>
        ))}
      </div>
    </div>
  );
};

MainLayout.propTypes = {
  // Children are implicitly handled by Outlet
};

export default MainLayout;
