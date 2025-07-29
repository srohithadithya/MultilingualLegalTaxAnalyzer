// frontend/src/utils/validationUtils.js

/**
 * Basic email validation regex.
 * @param {string} email
 * @returns {boolean}
 */
export const isValidEmail = (email) => {
  if (typeof email !== 'string') return false;
  const emailRegex = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;
  return emailRegex.test(email);
};

/**
 * Validates password strength based on criteria.
 * Matches backend's requirements for consistency.
 * @param {string} password
 * @param {object} options
 * @returns {{isValid: boolean, message: string}}
 */
export const validatePasswordStrength = (password, options = {}) => {
  const defaultOptions = {
    minLength: 8,
    requireDigit: true,
    requireUppercase: true,
    requireLowercase: true,
    requireSpecialChar: true,
  };
  const settings = { ...defaultOptions, ...options };

  if (typeof password !== 'string') {
    return { isValid: false, message: 'Password must be a string.' };
  }
  if (password.length < settings.minLength) {
    return { isValid: false, message: `Password must be at least ${settings.minLength} characters long.` };
  }
  if (settings.requireDigit && !/\d/.test(password)) {
    return { isValid: false, message: 'Password must contain at least one digit.' };
  }
  if (settings.requireUppercase && !/[A-Z]/.test(password)) {
    return { isValid: false, message: 'Password must contain at least one uppercase letter.' };
  }
  if (settings.requireLowercase && !/[a-z]/.test(password)) {
    return { isValid: false, message: 'Password must contain at least one lowercase letter.' };
  }
  if (settings.requireSpecialChar && !/[!@#$%^&*(),.?":{}|<>]/.test(password)) {
    return { isValid: false, message: 'Password must contain at least one special character.' };
  }

  return { isValid: true, message: 'Password meets strength requirements.' };
};

/**
 * Checks if a string is not empty or just whitespace.
 * @param {string} value
 * @returns {boolean}
 */
export const isNotEmpty = (value) => {
  return typeof value === 'string' && value.trim() !== '';
};