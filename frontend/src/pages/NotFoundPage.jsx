// frontend/src/pages/NotFoundPage.jsx

import React from 'react';
import { Link } from 'react-router-dom';
import styles from './NotFoundPage.module.scss'; // Component-specific styles

/**
 * NotFoundPage component for displaying a 404 error.
 */
const NotFoundPage = () => {
  return (
    <div className={styles.notFoundPage}>
      <h1 className={styles.title}>404</h1>
      <p className={styles.message}>Oops! The page you're looking for doesn't exist.</p>
      <Link to="/" className={styles.homeLink}>Go to Home Page</Link>
    </div>
  );
};

export default NotFoundPage;