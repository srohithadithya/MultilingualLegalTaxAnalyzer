// frontend/src/pages/DashboardPage/DashboardPage.jsx

import React, { useEffect } from 'react';
import { useAuth } from '../../features/auth/hooks/useAuth'; // Get user info
import { useDocumentAnalysis } from '../../features/document-analysis/hooks/useDocumentAnalysis.jsx'; // Document analysis hook
import { useMessage } from '../../store/messageStore'; // Global message context
import DocumentUploader from '../../features/document-analysis/components/DocumentUploader';
import PreviousAnalysisTable from '../../features/document-analysis/components/PreviousAnalysisTable';
import styles from './DashboardPage.module.scss';

/**
 * DashboardPage displays the user's welcome message, document uploader,
 * and a table of previously analyzed documents.
 */
const DashboardPage = () => {
  const { user } = useAuth(); // Current logged-in user
  const {
    documents,
    loading,
    uploading, // Separate loading state for upload
    error,
    message,
    fetchPreviousAnalyses,
    clearMessages,
  } = useDocumentAnalysis(); // Hook for document analysis features

  const { addMessage } = useMessage(); // Global message dispatcher

  // Fetch documents on component mount
  useEffect(() => {
    fetchPreviousAnalyses();
  }, [fetchPreviousAnalyses]);

  // Display global messages from useDocumentAnalysis
  useEffect(() => {
    if (error) {
      addMessage(error, 'error');
      clearMessages();
    }
    if (message) {
      addMessage(message, 'info'); // Or 'success' if it's a success message
      clearMessages();
    }
  }, [error, message, addMessage, clearMessages]);


  const handleUploadSuccess = (analysisResult) => {
    addMessage('Document uploaded and analysis initiated!', 'success');
    // Optionally, navigate directly to the analysis result page
    // navigate(`/analysis/${analysisResult.document_id}`);
    // Or just let the table refresh with the new document.
  };

  return (
    <div className={styles.dashboardPage}>
      <h1 className={styles.welcomeMessage}>Welcome, {user?.username || 'User'}!</h1>
      <p className={styles.introText}>Here you can upload new tax documents for analysis or review your past records.</p>

      <section className={styles.uploadSection}>
        <DocumentUploader onUploadSuccess={handleUploadSuccess} />
      </section>

      <section className={styles.historySection}>
        <PreviousAnalysisTable
          documents={documents}
          isLoading={loading || uploading} // Combine loading states for table
          error={error}
          message={message}
        />
      </section>
    </div>
  );
};

export default DashboardPage;
