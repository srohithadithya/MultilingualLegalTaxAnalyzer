// frontend/src/components/DataTable/DataTable.jsx

import React from 'react';
import PropTypes from 'prop-types';
import styles from './DataTable.module.scss'; // Import SCSS module

/**
 * Reusable DataTable component.
 * Displays data in a sortable, paginatable table structure.
 * (Sorting and pagination logic would be added here or passed via props).
 *
 * @param {Array<Object>} data - Array of objects, each representing a row.
 * @param {Array<Object>} columns - Array of column definitions: { key: string, label: string, render?: (item) => React.Node }.
 * @param {string} keyField - The key in each data item that serves as a unique ID (e.g., 'id').
 * @param {string} emptyMessage - Message to display when data is empty.
 * @param {boolean} isLoading - Whether data is currently loading.
 * @param {React.Node} loadingSpinner - Custom loading spinner component.
 */
const DataTable = ({
  data,
  columns,
  keyField = 'id', // Default field for unique key
  emptyMessage = 'No data available.',
  isLoading = false,
  loadingSpinner, // Optional custom loading spinner
  className = '', // Additional custom class names
}) => {
  if (isLoading) {
    return (
      <div className={styles.loadingContainer}>
        {loadingSpinner || <p>Loading data...</p>} {/* Or use a dedicated LoadingSpinner component */}
      </div>
    );
  }

  if (!data || data.length === 0) {
    return <div className={styles.emptyMessage}>{emptyMessage}</div>;
  }

  return (
    <div className={`${styles.tableContainer} ${className}`}>
      <table className={styles.table}>
        <thead>
          <tr>
            {columns.map((col) => (
              <th key={col.key} className={styles.headerCell}>
                {col.label}
                {/* Add sorting indicators here later */}
              </th>
            ))}
          </tr>
        </thead>
        <tbody>
          {data.map((item) => (
            <tr key={item[keyField]} className={styles.dataRow}>
              {columns.map((col) => (
                <td key={`${item[keyField]}-${col.key}`} className={styles.dataCell}>
                  {/* If a custom render function is provided, use it */}
                  {col.render ? col.render(item) : item[col.key]}
                </td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
      {/* Add pagination controls here later */}
    </div>
  );
};

DataTable.propTypes = {
  data: PropTypes.arrayOf(PropTypes.object).isRequired,
  columns: PropTypes.arrayOf(
    PropTypes.shape({
      key: PropTypes.string.isRequired,
      label: PropTypes.string.isRequired,
      render: PropTypes.func, // Optional custom render function for cell content
    })
  ).isRequired,
  keyField: PropTypes.string,
  emptyMessage: PropTypes.string,
  isLoading: PropTypes.bool,
  loadingSpinner: PropTypes.node,
  className: PropTypes.string,
};

export default DataTable;