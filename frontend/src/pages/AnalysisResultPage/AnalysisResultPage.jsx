// frontend/src/pages/AnalysisResultPage/AnalysisResultPage.jsx

import React, { useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom'; // useParams to get ID from URL
import { useDocumentAnalysis } from '../../features/document-analysis/hooks/useDocumentAnalysis';
import { useMessage } from '../../store/messageStore';
import AnalysisDisplay from '../../features/document-analysis/components/AnalysisDisplay';
import Button from '../../components/Button/Button';
import styles from './AnalysisResultPage.module.scss';

/**
 * AnalysisResultPage component fetches and displays the detailed analysis
 * for a specific document ID from the URL parameters.
 */
const AnalysisResultPage = () => {
  const { documentId } = useParams(); // Get documentId from URL (e.g., /analysis/123)
  const navigate = useNavigate();
  const {
    currentAnalysis,
    loading,
    error,
    message,
    clearMessages,
  } = useDocumentAnalysis(); // Hook for document analysis features

  const { addMessage } = useMessage(); // Global message dispatcher

  // Display global messages from useDocumentAnalysis
  useEffect(() => {
    if (error) {
      addMessage(error, 'error');
      clearMessages();
    }
    if (message) {
      addMessage(message, 'info'); // Or 'success'
      clearMessages();
    }
  }, [error, message, addMessage, clearMessages]);


  // Effect to ensure documentId is valid (optional, backend also validates)
  useEffect(() => {
    if (!documentId) {
      addMessage('No document ID provided for analysis.', 'error');
      navigate('/dashboard', { replace: true });
    }
  }, [documentId, addMessage, navigate]);

  return (
    <div className={styles.analysisResultPage}>
      <Button
        onClick={() => navigate('/dashboard')}
        variant="outline"
        size="sm"
        className={styles.backButton}
      >
        &larr; Back to Dashboard
      </Button>

      {documentId && <AnalysisDisplay documentId={documentId} />}

      {!loading && !error && !currentAnalysis && (
        <p className={styles.noData}>No analysis loaded. Please select a document from the dashboard.</p>
      )}
    </div>
  );
};

export default AnalysisResultPage;