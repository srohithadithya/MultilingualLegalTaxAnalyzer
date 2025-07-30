// frontend/src/store/appStore.jsx

import React, { createContext, useContext, useState, useCallback } from 'react';
import PropTypes from 'prop-types';

export const AppContext = createContext(null);

/**
 * AppProvider component manages general application-wide state.
 * Examples: global loading, theme preferences.
 */
export const AppProvider = ({ children }) => {
  const [globalLoading, setGlobalLoading] = useState(false);
  const [currentTheme, setCurrentTheme] = useState('light');

  const toggleTheme = useCallback(() => {
    setCurrentTheme((prevTheme) => {
      const newTheme = prevTheme === 'light' ? 'dark' : 'light';
      // Optional: Persist theme preference to localStorage
      // localStorage.setItem('appTheme', newTheme);
      return newTheme;
    });
  }, []);

  const contextValue = {
    globalLoading,
    setGlobalLoading,
    currentTheme,
    toggleTheme,
  };

  return (
    <AppContext.Provider value={contextValue}>
      {children}
    </AppContext.Provider>
  );
};

AppProvider.propTypes = {
  children: PropTypes.node.isRequired,
};

export const useAppContext = () => {
  const context = useContext(AppContext);
  if (context === undefined) {
    throw new Error('useAppContext must be used within an AppProvider');
  }
  return context;
};
