// frontend/src/features/document-analysis/analysisService.js

import documentApi from '../../services/documentApi'; // Import the specific document API client

const analysisService = {
  /**
   * Fetches all documents and their summary analysis for the current user's dashboard.
   * This is a direct pass-through to the documentApi.
   * @returns {Promise<object>} Dashboard data including documents list.
   */
  getPreviousAnalyses: async () => {
    return documentApi.getDashboardDocuments();
  },

  /**
   * Uploads a document and initiates its analysis.
   * This is a direct pass-through to the documentApi.
   * @param {File} file - The document file to upload.
   * @returns {Promise<object>} The response data from the upload and analysis initiation.
   */
  uploadAndAnalyzeDocument: async (file) => {
    return documentApi.uploadDocument(file);
  },

  /**
   * Fetches the detailed analysis results for a specific document ID.
   * This is a direct pass-through to the documentApi.
   * @param {string} documentId - The ID of the document to fetch analysis for.
   * @returns {Promise<object>} The detailed analysis data.
   */
  getDetailedAnalysis: async (documentId) => {
    return documentApi.getAnalysisResult(documentId);
  },

  /**
   * Triggers the download of a PDF report for a given document.
   * @param {string} documentId - The ID of the document.
   * @param {string} lang - The desired language code for the PDF.
   * @returns {Promise<object>} Success status.
   */
  downloadAnalysisPdf: async (documentId, lang) => {
    return documentApi.downloadPdfReport(documentId, lang);
  },

  /**
   * Fetches an audio URL for the analysis of a given document.
   * @param {string} documentId - The ID of the document.
   * @param {string} lang - The desired language code for the speech audio.
   * @returns {Promise<string>} A Blob URL to the audio file.
   */
  getAnalysisSpeech: async (documentId, lang) => {
    return documentApi.getSpeechAudio(documentId, lang);
  },

  // You can add more complex, feature-specific logic here if needed,
  // e.g., combining multiple API calls or pre-processing data before returning.
};

export default analysisService;