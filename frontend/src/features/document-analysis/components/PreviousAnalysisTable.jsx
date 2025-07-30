// frontend/src/features/document-analysis/components/PreviousAnalysisTable.jsx

import React from 'react';
import PropTypes from 'prop-types';
import DataTable from '../../../components/DataTable/DataTable'; // Reusable DataTable
import Button from '../../../components/Button/Button';
import LoadingSpinner from '../../../components/LoadingSpinner/LoadingSpinner';
import { formatDate } from '../../../utils/dateUtils'; // Utility for date formatting
import { useNavigate } from 'react-router-dom'; // For navigation
import { useDocumentAnalysis } from '../hooks/useDocumentAnalysis.jsx';
import styles from './PreviousAnalysisTable.module.scss'; // Component-specific styles

/**
 * Displays a table of previously analyzed documents for the user.
 * Allows viewing details, downloading PDF, and playing speech.
 */
const PreviousAnalysisTable = ({ documents, isLoading, error, message }) => {
  const navigate = useNavigate();

  // Define columns for the DataTable component
  const columns = [
    { key: 'filename', label: 'Document Name' },
    {
      key: 'upload_date',
      label: 'Upload Date',
      render: (item) => formatDate(item.upload_date, { year: 'numeric', month: 'short', day: 'numeric', hour: '2-digit', minute: '2-digit' }),
    },
    { key: 'invoice_number', label: 'Invoice No.', render: (item) => item.summary?.invoice_number || 'N/A' },
    { key: 'vendor_name', label: 'Vendor', render: (item) => item.summary?.vendor_name || 'N/A' },
    {
      key: 'total_amount',
      label: 'Total Amount',
      render: (item) => (item.summary?.total_amount ? `${item.summary.currency || ''} ${item.summary.total_amount}` : 'N/A'),
    },
    {
      key: 'actions',
      label: 'Actions',
      render: (item) => (
        <div className={styles.actionButtons}>
          <Button
            variant="primary"
            size="sm"
            onClick={() => navigate(`/analysis/${item.id}`)} // Navigate to detailed analysis page
            disabled={!item.has_analysis} // Disable if no analysis data yet
          >
            View Details
          </Button>
          {/* PDF and Speech buttons will be on the detailed analysis page */}
        </div>
      ),
    },
  ];

  if (error) {
    return <p className={styles.errorMessage}>Error: {error}</p>;
  }

  return (
    <div className={styles.tableSection}>
      <h3>Your Analyzed Documents</h3>
      {message && !error && <p className={styles.infoMessage}>{message}</p>}
      <DataTable
        data={documents}
        columns={columns}
        keyField="id"
        emptyMessage="No documents analyzed yet. Upload one above!"
        isLoading={isLoading}
        loadingSpinner={<LoadingSpinner size="md" color="primary" />}
        className={styles.dashboardTable}
      />
    </div>
  );
};

PreviousAnalysisTable.propTypes = {
  documents: PropTypes.arrayOf(PropTypes.object).isRequired,
  isLoading: PropTypes.bool.isRequired,
  error: PropTypes.string,
  message: PropTypes.string,
};

export default PreviousAnalysisTable;
