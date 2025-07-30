// frontend/src/App.jsx

import React from 'react';
import AppRouter from './router/AppRouter'; // Import your AppRouter
import { AuthProvider } from './features/auth/AuthProvider'; // Import AuthProvider
import { MessageProvider } from './store/messageStore.jsx'; // Import MessageProvider
import { AppProvider } from './store/appStore'; // Import AppProvider

/**
 * The root component of the application.
 * Wraps the entire app with necessary context providers and the router.
 */
function App() {
  return (
    // Order of providers might matter if one depends on another (e.g., MessageProvider might need Auth info)
    <AppProvider> {/* General app settings */}
      <AuthProvider> {/* Authentication state */}
        <MessageProvider> {/* Global messages/toasts */}
          <AppRouter /> {/* Defines all routes and renders pages */}
        </MessageProvider>
      </AuthProvider>
    </AppProvider>
  );
}

export default App;
