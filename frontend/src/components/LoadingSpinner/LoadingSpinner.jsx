// frontend/src/components/LoadingSpinner/LoadingSpinner.jsx

import React from 'react';
import PropTypes from 'prop-types';
import styles from './LoadingSpinner.module.scss'; // Import SCSS module

/**
 * Reusable Loading Spinner component.
 * Displays a visual indicator during asynchronous operations.
 */
const LoadingSpinner = ({ size = 'md', color = 'primary', className = '' }) => {
  const spinnerClasses = [
    styles.spinner,
    styles[size],   // 'sm', 'md', 'lg'
    styles[color],  // 'primary', 'secondary', 'white', 'dark'
    className
  ].filter(Boolean).join(' ');

  return (
    <div className={spinnerClasses} role="status" aria-label="Loading">
      <span className="visually-hidden">Loading...</span> {/* Accessible text */}
    </div>
  );
};

LoadingSpinner.propTypes = {
  size: PropTypes.oneOf(['sm', 'md', 'lg', 'xl']), // Added 'xl' for more flexibility
  color: PropTypes.oneOf(['primary', 'secondary', 'white', 'dark']),
  className: PropTypes.string,
};

export default LoadingSpinner;