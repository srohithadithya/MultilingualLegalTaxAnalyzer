// frontend/src/utils/dateUtils.js

/**
 * Formats a Date object or ISO string into a human-readable date.
 * @param {Date|string} dateInput - The date to format.
 * @param {object} options - Intl.DateTimeFormat options.
 * @returns {string} The formatted date string.
 */
export const formatDate = (dateInput, options = {}) => {
  if (!dateInput) return 'N/A';
  const date = typeof dateInput === 'string' ? new Date(dateInput) : dateInput;
  if (isNaN(date.getTime())) { // Check for invalid date
    return 'Invalid Date';
  }
  const defaultOptions = { year: 'numeric', month: 'short', day: 'numeric' };
  return new Intl.DateTimeFormat('en-US', { ...defaultOptions, ...options }).format(date);
};

/**
 * Formats a Date object or ISO string into a time string.
 * @param {Date|string} dateInput - The date to format.
 * @returns {string} The formatted time string.
 */
export const formatTime = (dateInput) => {
  if (!dateInput) return 'N/A';
  const date = typeof dateInput === 'string' ? new Date(dateInput) : dateInput;
  if (isNaN(date.getTime())) {
    return 'Invalid Time';
  }
  return new Intl.DateTimeFormat('en-US', { hour: 'numeric', minute: 'numeric', hour12: true }).format(date);
};

/**
 * Formats a Date object or ISO string into a full date and time string.
 * @param {Date|string} dateInput - The date to format.
 * @returns {string} The formatted date and time string.
 */
export const formatDateTime = (dateInput) => {
  if (!dateInput) return 'N/A';
  const date = typeof dateInput === 'string' ? new Date(dateInput) : dateInput;
  if (isNaN(date.getTime())) {
    return 'Invalid DateTime';
  }
  return formatDate(date, { year: 'numeric', month: 'short', day: 'numeric', hour: 'numeric', minute: 'numeric', hour12: true });
};