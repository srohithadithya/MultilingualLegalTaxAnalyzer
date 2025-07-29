// frontend/src/components/Button/Button.jsx

import React from 'react';
import PropTypes from 'prop-types';
import styles from './Button.module.scss'; // Import SCSS module

/**
 * Reusable Button component.
 * Supports different styles, sizes, and states.
 */
const Button = ({
  children,
  onClick,
  type = 'button', // Default to 'button' to prevent unintended form submission
  variant = 'primary', // 'primary', 'secondary', 'outline', 'text', 'danger', 'success'
  size = 'md',        // 'sm', 'md', 'lg'
  disabled = false,
  isLoading = false, // For loading state with spinner
  className = '',     // Additional custom class names
  ...props            // Any other standard button props (e.g., aria-label)
}) => {
  const buttonClasses = [
    styles.button,
    styles[variant], // Apply variant specific style
    styles[size],    // Apply size specific style
    disabled || isLoading ? styles.disabled : '', // Apply disabled style if disabled or loading
    className        // Apply any custom class passed in
  ].filter(Boolean).join(' '); // Filter out empty strings and join

  return (
    <button
      className={buttonClasses}
      onClick={onClick}
      type={type}
      disabled={disabled || isLoading}
      {...props}
    >
      {isLoading ? (
        <span className={styles.spinner}></span> // Simple CSS spinner
      ) : (
        children
      )}
    </button>
  );
};

Button.propTypes = {
  children: PropTypes.node.isRequired, // Button content (text, icon, etc.)
  onClick: PropTypes.func,             // Click handler
  type: PropTypes.oneOf(['button', 'submit', 'reset']), // HTML button type
  variant: PropTypes.oneOf(['primary', 'secondary', 'outline', 'text', 'danger', 'success']),
  size: PropTypes.oneOf(['sm', 'md', 'lg']),
  disabled: PropTypes.bool,
  isLoading: PropTypes.bool,
  className: PropTypes.string,
};

export default Button;