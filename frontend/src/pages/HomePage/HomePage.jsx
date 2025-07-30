// frontend/src/pages/HomePage/HomePage.jsx

import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '~features/auth/hooks/useAuth.jsx'; // Updated import path and .jsx
import { useMessage } from '~store/messageStore.jsx'; // Updated import path and .jsx
import LoginForm from '~features/auth/components/LoginForm.jsx'; // Updated import path and .jsx
import SignupForm from '~features/auth/components/SignupForm.jsx'; // Updated import path and .jsx

// Import SVG as a React Component using '?react' suffix for vite-plugin-svgr
import AnalyzerLogo from '~assets/images/analyzer-logo.svg?react'; // Updated import path and ?react

import styles from './HomePage.module.scss';

/**
 * The application's landing/introduction page.
 * Displays a hero section, value proposition, and switches between Login and Signup forms.
 */
const HomePage = () => {
  const { isAuthenticated, loading: authLoading } = useAuth();
  const { addMessage } = useMessage();
  const navigate = useNavigate();
  const [isLoginView, setIsLoginView] = useState(true);

  useEffect(() => {
    if (isAuthenticated && !authLoading) {
      navigate('/dashboard', { replace: true });
    }
  }, [isAuthenticated, authLoading, navigate]);

  const handleLoginSuccess = () => {
    addMessage('Login successful! Welcome back.', 'success');
    navigate('/dashboard');
  };

  const handleSignupSuccess = (message) => {
    addMessage(message || 'Account created successfully. Please login.', 'success');
    setIsLoginView(true);
  };

  if (authLoading) {
    return null;
  }

  return (
    <div className={styles.homePage}>
      <section className={styles.heroSection}>
        <div className={styles.heroContent}>
          {/* Use the SVG as a React component */}
          <AnalyzerLogo className={styles.heroLogo} /> {/* Apply custom class for styling */}
          <h1 className={styles.heroTitle}>Multi-Lingual Legal Tax Analyzer</h1>
          <p className={styles.heroSubtitle}>
            Unlock seamless tax document processing with AI-powered multi-lingual analysis,
            accurate data extraction, and intuitive reporting.
          </p>
          <div className={styles.ctaButtons}>
            <button className={styles.mainCtaButton} onClick={() => setIsLoginView(true)}>Get Started</button>
            <button className={styles.secondaryCtaButton}>Learn More</button>
          </div>
        </div>
      </section>

      <section className={styles.featuresSection}>
        <h2>Why Our Analyzer?</h2>
        <div className={styles.featureGrid}>
          <div className={styles.featureCard}>
            <h3>Hybrid AI Accuracy</h3>
            <p>Combines Tesseract OCR with Ollama Vision for unparalleled data extraction precision.</p>
          </div>
          <div className={styles.featureCard}>
            <h3>Multilingual Support</h3>
            <p>Process documents and get reports in any language, breaking down barriers.</p>
          </div>
          <div className={styles.featureCard}>
            <h3>Structured Insights</h3>
            <p>Extracts dates, GST, names, totals, and more into actionable, organized formats.</p>
          </div>
          <div className={styles.featureCard}>
            <h3>Interactive Reports</h3>
            <p>Download professional PDFs and listen to your translated data via speech synthesis.</p>
          </div>
        </div>
      </section>

      <section className={styles.authSection}>
        <div className={styles.authFormWrapper}>
          {isLoginView ? (
            <LoginForm onSuccess={handleLoginSuccess} onSwitchToSignup={() => setIsLoginView(false)} />
          ) : (
            <SignupForm onSuccess={handleSignupSuccess} onSwitchToLogin={() => setIsLoginView(true)} />
          )}
        </div>
      </section>

      <footer className={styles.footer}>
        <p>&copy; {new Date().getFullYear()} Multi-Lingual Tax Analyzer. All rights reserved.</p>
      </footer>
    </div>
  );
};

export default HomePage;
