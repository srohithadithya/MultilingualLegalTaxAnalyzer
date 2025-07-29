// frontend/src/components/LanguageSelector/LanguageSelector.jsx

import React from 'react';
import PropTypes from 'prop-types';
import styles from './LanguageSelector.module.scss'; // Import SCSS module

/**
 * Reusable Language Selector dropdown.
 * Allows users to select a preferred language from a list of options.
 */
const LanguageSelector = ({ selectedLanguage, onLanguageChange, availableLanguages, label = "Select Language" }) => {
  return (
    <div className={styles.languageSelector}>
      {label && <label htmlFor="language-select" className={styles.label}>{label}</label>}
      <select
        id="language-select"
        className={styles.select}
        value={selectedLanguage}
        onChange={(e) => onLanguageChange(e.target.value)}
        aria-label={label}
      >
        {availableLanguages.map((lang) => (
          <option key={lang.code} value={lang.code}>
            {lang.name}
          </option>
        ))}
      </select>
    </div>
  );
};

LanguageSelector.propTypes = {
  selectedLanguage: PropTypes.string.isRequired,
  onLanguageChange: PropTypes.func.isRequired,
  availableLanguages: PropTypes.arrayOf(
    PropTypes.shape({
      code: PropTypes.string.isRequired, // e.g., 'en', 'hi', 'fr'
      name: PropTypes.string.isRequired, // e.g., 'English', 'हिन्दी', 'Français'
    })
  ).isRequired,
  label: PropTypes.string,
};

export default LanguageSelector;