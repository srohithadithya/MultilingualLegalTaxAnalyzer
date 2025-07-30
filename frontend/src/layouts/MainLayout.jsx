// frontend/src/layouts/MainLayout.jsx

import React from 'react';
import PropTypes from 'prop-types';
import { Outlet, Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../features/auth/hooks/useAuth'; // Import useAuth hook
import { useMessage } from '../store/messageStore.jsx'; // Import useMessage hook
import Button from '../components/Button/Button';
import LoadingSpinner from '../components/LoadingSpinner/LoadingSpinner'; // For global loading if needed
import analyzerLogo from '../assets/images/analyzer-logo.svg'; // Your logo asset
import styles from './MainLayout.module.scss'; // Module SCSS for this layout

/**
 * MainLayout component for authenticated users.
 * Includes a header, navigation, and renders child routes via <Outlet />.
 * Also displays global messages (toasts/alerts).
 */
const MainLayout = () => {
  const { user, logout, isAuthenticated } = useAuth(); // Get user and logout function
  const { messages, removeMessage } = useMessage(); // Get messages and functions
  const navigate = useNavigate();

  const handleLogout = async () => {
    try {
      await logout();
      navigate('/auth/login'); // Redirect to login after logout
    } catch (error) {
      console.error('Logout error:', error);
      // Message already handled by AuthProvider, but could add specific UI here
    }
  };

  // Only render children if authenticated. PrivateRoute in AppRouter handles redirect if not.
  if (!isAuthenticated) {
    // This case should primarily be handled by the AppRouter's PrivateRoute
    // For safety, a minimal loading or redirect message could be here
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
            <img src={analyzerLogo} alt="Analyzer Logo" className={styles.logo} />
            <span className={styles.appName}>Tax Analyzer</span>
          </Link>
          <nav className={styles.navbarNav}>
            <ul>
              <li><Link to="/dashboard">Dashboard</Link></li>
              {/* Add more authenticated nav links here */}
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
        <Outlet /> {/* Renders the current route's component */}
      </main>

      <footer className={styles.footer}>
        <p>&copy; {new Date().getFullYear()} Multi-Lingual Tax Analyzer. All rights reserved.</p>
        <p>Built with ❤️ by Your Team.</p>
      </footer>

      {/* Global Message Display (e.g., Toast notifications) */}
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
