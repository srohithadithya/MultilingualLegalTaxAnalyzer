// frontend/src/router/AppRouter.jsx

import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate, Outlet } from 'react-router-dom';
import PropTypes from 'prop-types';
import { useAuth } from '../features/auth/hooks/useAuth'; // Import useAuth hook
import HomePage from '../pages/HomePage/HomePage';
import DashboardPage from '../pages/DashboardPage/DashboardPage';
import AnalysisResultPage from '../pages/AnalysisResultPage/AnalysisResultPage';
import NotFoundPage from '../pages/NotFoundPage';
import MainLayout from '../layouts/MainLayout'; // Authenticated layout
import AuthLayout from '../layouts/AuthLayout'; // Auth pages layout

/**
 * PrivateRoute component to protect routes that require authentication.
 * If not authenticated, redirects to the login page.
 */
const PrivateRoute = ({ children }) => {
  const { isAuthenticated, loading } = useAuth();

  // Show nothing while authentication status is being checked
  if (loading) {
    return null; // AuthProvider already shows a global spinner
  }

  // If authenticated, render the child routes/components
  if (isAuthenticated) {
    return children ? children : <Outlet />;
  }

  // If not authenticated, redirect to the login page (HomePage in this case)
  return <Navigate to="/" replace />;
};

PrivateRoute.propTypes = {
  children: PropTypes.node,
};

/**
 * AppRouter defines all the routes for the application.
 * It uses BrowserRouter and organizes routes into public and private sections.
 */
const AppRouter = () => {
  return (
    <Router>
      <Routes>
        {/* Public Routes - Use AuthLayout */}
        <Route element={<AuthLayout />}>
          <Route path="/" element={<HomePage />} /> {/* Landing page with login/signup */}
          {/* If you wanted a dedicated /auth/login or /auth/signup page instead of toggling on HomePage */}
          {/* <Route path="/auth/login" element={<LoginPage />} /> */}
          {/* <Route path="/auth/signup" element={<SignupPage />} /> */}
        </Route>

        {/* Private Routes - Use MainLayout and PrivateRoute protection */}
        <Route element={<PrivateRoute><MainLayout /></PrivateRoute>}>
          <Route path="/dashboard" element={<DashboardPage />} />
          <Route path="/analysis/:documentId" element={<AnalysisResultPage />} />
          {/* Add more authenticated routes here */}
        </Route>

        {/* Catch-all route for 404 Not Found */}
        <Route path="*" element={<NotFoundPage />} />
      </Routes>
    </Router>
  );
};

export default AppRouter;