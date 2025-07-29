// frontend/src/store/appStore.js

import React, { createContext, useContext, useState, useCallback } from 'react';
import PropTypes from 'prop-types';

// Create the AppContext
export const AppContext = createContext(null);

/**
 * AppProvider component manages general application-wide state.
 * Examples: global loading, theme preferences.
 */
export const AppProvider = ({ children }) => {
  const [globalLoading, setGlobalLoading] = useState(false); // For full-screen loading, not specific API calls
  const [currentTheme, setCurrentTheme] = useState('light'); // Example: 'light' or 'dark' theme

  /**
   * Toggles the application's theme between 'light' and 'dark'.
   */
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

  return (
    <AppContext.Provider value={contextValue}>
      {children}
    </AppContext.Provider>
  );
};

AppProvider.propTypes = {
  children: PropTypes.node.isRequired,
};

/**
 * Custom hook to consume the AppContext.
 * @returns {{globalLoading: boolean, setGlobalLoading: Function, currentTheme: string, toggleTheme: Function}}
 */
export const useAppContext = () => {
  const context = useContext(AppContext);
  if (context === undefined) {
    throw new Error('useAppContext must be used within an AppProvider');
  }
  return context;
};