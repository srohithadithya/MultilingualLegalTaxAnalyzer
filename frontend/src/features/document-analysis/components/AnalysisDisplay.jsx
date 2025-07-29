// frontend/src/features/document-analysis/components/AnalysisDisplay.jsx

import React, { useState, useEffect } from 'react';
import PropTypes from 'prop-types';
import Button from '../../../components/Button/Button';
import LoadingSpinner from '../../../components/LoadingSpinner/LoadingSpinner';
import LanguageSelector from '../../../components/LanguageSelector/LanguageSelector';
import { useDocumentAnalysis } from '../hooks/useDocumentAnalysis'; // Our analysis hook
import { formatDate } from '../../../utils/dateUtils';
import styles from './AnalysisDisplay.module.scss';

/**
 * Displays the detailed analysis results of a single document.
 * Provides options to download PDF report and play speech audio in different languages.
 */
const AnalysisDisplay = ({ documentId }) => {
  const {
    currentAnalysis,
    loading,
    error,
    message,
    fetchDetailedAnalysis,
    downloadPdf,
    playSpeech,
    clearMessages,
  } = useDocumentAnalysis();

  const [selectedOutputLanguage, setSelectedOutputLanguage] = useState('en'); // Default to English

  // Fetch detailed analysis when component mounts or documentId changes
  useEffect(() => {
    if (documentId) {
      fetchDetailedAnalysis(documentId);
    }
  }, [documentId, fetchDetailedAnalysis]);

  // Set default output language from fetched analysis if available
  useEffect(() => {
    if (currentAnalysis && currentAnalysis.preferred_language) {
      setSelectedOutputLanguage(currentAnalysis.preferred_language);
    }
  }, [currentAnalysis]);

  const availableLanguages = [
    { code: 'en', name: 'English' },
    { code: 'hi', name: 'हिन्दी' },
    { code: 'fr', name: 'Français' },
    { code: 'es', name: 'Español' },
    // Add more languages as supported by your backend's translation/TTS services
  ];

  if (loading) {
    return (
      <div className={styles.loadingWrapper}>
        <LoadingSpinner size="lg" />
        <p>Loading analysis...</p>
      </div>
    );
  }

  if (error) {
    return <p className={styles.errorMessage}>Error: {error}</p>;
  }

  if (!currentAnalysis || !currentAnalysis.analyzed_data) {
    return <p className={styles.noDataMessage}>No analysis data found for this document.</p>;
  }

  const data = currentAnalysis.analyzed_data;

  // Function to render an individual data field
  const renderDataField = (label, value) => {
    if (value === null || value === undefined || value === '') return null;
    return (
      <div className={styles.dataField}>
        <strong>{label}:</strong> {value}
      </div>
    );
  };

  return (
    <div className={styles.analysisDisplay}>
      <h2 className={styles.title}>Analysis Result: {currentAnalysis.filename}</h2>
      <p className={styles.analyzedAt}>Analyzed on: {formatDate(currentAnalysis.analyzed_at, { dateStyle: 'medium', timeStyle: 'short' })}</p>

      {message && !error && <p className={styles.successMessage}>{message}</p>}
      {error && <p className={styles.errorMessage}>{error}</p>}


      <div className={styles.outputControls}>
        <LanguageSelector
          selectedLanguage={selectedOutputLanguage}
          onLanguageChange={(lang) => {
            setSelectedOutputLanguage(lang);
            clearMessages(); // Clear messages on language change
          }}
          availableLanguages={availableLanguages}
          label="Output Language"
        />
        <Button
          onClick={() => downloadPdf(documentId, selectedOutputLanguage)}
          isLoading={loading} // Use general loading for now, or separate for actions
          disabled={loading}
          variant="outline"
          size="md"
        >
          Download PDF
        </Button>
        <Button
          onClick={() => playSpeech(documentId, selectedOutputLanguage)}
          isLoading={loading}
          disabled={loading}
          variant="secondary"
          size="md"
        >
          Play Speech
        </Button>
      </div>

      <div className={styles.section}>
        <h3>Basic Information</h3>
        {renderDataField('Document Type', data.document_type)}
        {renderDataField('Invoice Number', data.invoice_number)}
        {renderDataField('Date', data.date)}
        {renderDataField('Due Date', data.due_date)}
        {renderDataField('Currency', data.currency)}
        {renderDataField('Extracted Language', data.extracted_language)}
        {renderDataField('Accuracy Confidence', data.accuracy_confidence)}
        {renderDataField('Payment Terms', data.payment_terms)}
        {renderDataField('Notes', data.notes)}
      </div>

      <div className={styles.section}>
        <h3>Parties Involved</h3>
        <div className={styles.partiesGrid}>
          <div>
            <h4>Vendor Details</h4>
            {renderDataField('Name', data.vendor_name)}
            {renderDataField('Address', data.vendor_address)}
            {renderDataField('Tax ID', data.vendor_tax_id)}
          </div>
          <div>
            <h4>Customer Details</h4>
            {renderDataField('Name', data.customer_name)}
            {renderDataField('Address', data.customer_address)}
            {renderDataField('Tax ID', data.customer_tax_id)}
          </div>
        </div>
      </div>

      <div className={styles.section}>
        <h3>Financial Summary</h3>
        {renderDataField('Subtotal', data.subtotal_amount)}
        {renderDataField('Tax Amount', data.tax_amount)}
        {renderDataField('Total Amount', data.total_amount)}
      </div>

      {data.line_items && data.line_items.length > 0 && (
        <div className={styles.section}>
          <h3>Line Items</h3>
          <div className={styles.lineItemsTable}>
            <table>
              <thead>
                <tr>
                  <th>Description</th>
                  <th>Quantity</th>
                  <th>Unit Price</th>
                  <th>Total Price</th>
                </tr>
              </thead>
              <tbody>
                {data.line_items.map((item, index) => (
                  <tr key={index}>
                    <td>{item.description || 'N/A'}</td>
                    <td>{item.quantity || 'N/A'}</td>
                    <td>{item.unit_price || 'N/A'}</td>
                    <td>{item.total_price || 'N/A'}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}

      {(data.validation_errors && Object.keys(data.validation_errors).length > 0) && (
        <div className={`${styles.section} ${styles.errorSection}`}>
          <h3>Validation Errors</h3>
          <ul>
            {Object.entries(data.validation_errors).map(([key, value]) => (
              <li key={key}><strong>{key}:</strong> {value}</li>
            ))}
          </ul>
        </div>
      )}

      {(data.warnings && Object.keys(data.warnings).length > 0) && (
        <div className={`${styles.section} ${styles.warningSection}`}>
          <h3>Warnings</h3>
          <ul>
            {Object.entries(data.warnings).map(([key, value]) => (
              <li key={key}><strong>{key}:</strong> {value}</li>
            ))}
          </ul>
        </div>
      )}

      {data.raw_ocr_text_reference && (
        <div className={styles.section}>
          <h3>Raw Document Snippet</h3>
          <pre className={styles.rawTextSnippet}>{data.raw_ocr_text_reference}</pre>
        </div>
      )}
    </div>
  );
};

AnalysisDisplay.propTypes = {
  documentId: PropTypes.string.isRequired,
};

export default AnalysisDisplay;