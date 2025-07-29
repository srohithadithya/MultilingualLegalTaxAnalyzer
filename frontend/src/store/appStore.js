// frontend/src/store/appStore.js

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

  // Effect to load theme from localStorage on initial mount (if persisted)
  // useEffect(() => {
  //   const storedTheme = localStorage.getItem('appTheme');
  //   if (storedTheme && (storedTheme === 'light' || storedTheme === 'dark')) {
  //     setCurrentTheme(storedTheme);
  //   }
  // }, []);


  const contextValue = {
    globalLoading,
    setGlobalLoading,
    currentTheme,
    toggleTheme,
  };

  // Ensure this return block is exactly as shown, with proper indentation
  // No extra characters or weird newlines before `<AppContext.Provider`
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
