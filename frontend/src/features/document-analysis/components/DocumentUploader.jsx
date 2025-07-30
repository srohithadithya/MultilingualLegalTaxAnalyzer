// frontend/src/features/document-analysis/components/DocumentUploader.jsx

import React, { useState, useRef } from 'react';
import PropTypes from 'prop-types';
import Button from '../../../components/Button/Button';
import LoadingSpinner from '../../../components/LoadingSpinner/LoadingSpinner';
import { useDocumentAnalysis } from '../hooks/useDocumentAnalysis.jsx'; // Import our analysis hook
import styles from './DocumentUploader.module.scss';
import UploadIcon from '../../assets/icons/upload-icon.svg';

/**
 * DocumentUploader component provides a drag-and-drop interface for file uploads.
 * It integrates with the useDocumentAnalysis hook for backend interaction.
 */
const DocumentUploader = ({ onUploadSuccess }) => {
  const { uploadDocument, uploading, error, message, clearMessages } = useDocumentAnalysis();
  const [dragActive, setDragActive] = useState(false);
  const [selectedFile, setSelectedFile] = useState(null);
  const inputRef = useRef(null);

  const allowedFileTypes = ['application/pdf', 'image/png', 'image/jpeg', 'image/tiff'];

  const handleDrag = (e) => {
    e.preventDefault();
    e.stopPropagation();
    if (e.type === 'dragenter' || e.type === 'dragover') {
      setDragActive(true);
    } else if (e.type === 'dragleave') {
      setDragActive(false);
    }
  };

  const DocumentUploader = ({ /* ... */ }) => {
    return (
        <div className={styles.dragArea}>
            {/* ... other content ... */}
            <img src={UploadIcon} alt="Upload" className={styles.uploadIcon} /> {/* Use it like an image */}
            {/* OR to customize color via CSS 'currentColor' or props: */}
            {/* <UploadIcon className={styles.uploadIcon} /> */}
            <p>Drag & Drop your tax receipt/invoice here</p>
            {/* ... */}
        </div>
            );
    };
  const handleDrop = (e) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      const file = e.dataTransfer.files[0];
      if (allowedFileTypes.includes(file.type)) {
        setSelectedFile(file);
        clearMessages();
      } else {
        setSelectedFile(null);
        clearMessages(); // Clear existing success/error before showing new error
        alert('Unsupported file type. Please upload PDF, PNG, JPEG, or TIFF.');
      }
    }
  };

  const handleChange = (e) => {
    if (e.target.files && e.target.files[0]) {
      const file = e.target.files[0];
      if (allowedFileTypes.includes(file.type)) {
        setSelectedFile(file);
        clearMessages();
      } else {
        setSelectedFile(null);
        clearMessages();
        alert('Unsupported file type. Please upload PDF, PNG, JPEG, or TIFF.');
      }
    }
  };

  const onButtonClick = () => {
    inputRef.current.click(); // Trigger hidden input click
  };

  const handleUploadClick = async () => {
    if (selectedFile) {
      const analysisResult = await uploadDocument(selectedFile);
      if (analysisResult) {
        setSelectedFile(null); // Clear selected file after successful upload
        if (onUploadSuccess) {
          onUploadSuccess(analysisResult); // Pass analysis to parent if needed
        }
      }
    } else {
      alert('Please select a file to upload.');
    }
  };

  return (
    <div className={styles.uploaderContainer}>
      <h3>Upload New Document</h3>
      <div
        className={`${styles.dragArea} ${dragActive ? styles.dragActive : ''}`}
        onDragEnter={handleDrag}
        onDragLeave={handleDrag}
        onDragOver={handleDrag}
        onDrop={handleDrop}
      >
        <input
          type="file"
          id="file-input"
          ref={inputRef}
          onChange={handleChange}
          accept=".pdf,.png,.jpg,.jpeg,.tiff" // Accept attribute for file dialog
          className={styles.fileInput}
        />
        <p className={styles.dragText}>Drag & Drop your tax receipt/invoice here</p>
        <p className={styles.orText}>OR</p>
        <Button onClick={onButtonClick} variant="outline" size="md">
          Browse Files
        </Button>
        <p className={styles.supportedTypes}>Supported: PDF, PNG, JPG, JPEG, TIFF</p>
      </div>

      {selectedFile && (
        <div className={styles.selectedFileDisplay}>
          <p>Selected file: <strong>{selectedFile.name}</strong></p>
          <Button
            onClick={handleUploadClick}
            isLoading={uploading}
            disabled={uploading}
            variant="primary"
            size="md"
            className={styles.uploadButton}
          >
            {uploading ? 'Uploading & Analyzing...' : 'Upload & Analyze'}
          </Button>
        </div>
      )}

      {uploading && <LoadingSpinner size="sm" className={styles.uploadSpinner} />}
      {error && <p className={styles.errorMessage}>{error}</p>}
      {message && !error && <p className={styles.successMessage}>{message}</p>}
    </div>
  );
};

DocumentUploader.propTypes = {
  onUploadSuccess: PropTypes.func, // Callback when upload and initial analysis succeed
};

export default DocumentUploader;
