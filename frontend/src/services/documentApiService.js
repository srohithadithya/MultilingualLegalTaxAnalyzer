// frontend/src/services/documentApiService.js

import api from './api';

const BASE_DOCUMENTS_URL = '/documents';
const BASE_ANALYSIS_URL = '/analysis';

const documentApiService = {
  /**
   * Fetches all documents and their summary analysis for the current user.
   * Corresponds to GET /dashboard/my_documents
   */
  getDashboardDocuments: async () => {
    try {
      const response = await api.get('/dashboard/my_documents');
      return response.data;
    } catch (error) {
      console.error('Error fetching dashboard documents:', error);
      throw error;
    }
  },

  /**
   * Uploads a document for analysis.
   * Corresponds to POST /documents/upload
   * @param {File} file - The file to upload.
   */
  uploadDocument: async (file) => {
    try {
      const formData = new FormData();
      formData.append('document', file); // 'document' must match Flask's request.files key

      const response = await api.post(`${BASE_DOCUMENTS_URL}/upload`, formData, {
        headers: {
          'Content-Type': 'multipart/form-data', // Important for file uploads
        },
      });
      return response.data;
    } catch (error) {
      console.error('Error uploading document:', error);
      throw error;
    }
  },

  /**
   * Fetches detailed analysis results for a specific document.
   * Corresponds to GET /analysis/<document_id>
   * @param {string} documentId
   */
  getAnalysisResult: async (documentId) => {
    try {
      const response = await api.get(`${BASE_ANALYSIS_URL}/${documentId}`);
      return response.data;
    } catch (error) {
      console.error(`Error fetching analysis result for ${documentId}:`, error);
      throw error;
    }
  },

  /**
   * Initiates download of a PDF report for a document, optionally in a specific language.
   * Corresponds to GET /analysis/<document_id>/download_pdf?lang=<lang_code>
   * @param {string} documentId
   * @param {string} lang - The language for the PDF report (e.g., 'en', 'hi').
   */
  downloadPdfReport: async (documentId, lang = 'en') => {
    try {
      // Use arraybuffer responseType for binary files like PDFs
      const response = await api.get(`${BASE_ANALYSIS_URL}/${documentId}/download_pdf`, {
        params: { lang },
        responseType: 'arraybuffer', // Get response as a binary blob
      });

      // Create a Blob from the response data
      const blob = new Blob([response.data], { type: 'application/pdf' });
      // Get filename from Content-Disposition header if available, otherwise default
      const contentDisposition = response.headers['content-disposition'];
      let filename = `analysis_report_${documentId}.pdf`;
      if (contentDisposition && contentDisposition.indexOf('filename=') !== -1) {
        filename = contentDisposition.split('filename=')[1].split(';')[0].replace(/"/g, '');
      }

      // Create a URL for the blob and trigger download
      const url = window.URL.createObjectURL(blob);
      const link = document.createElement('a');
      link.href = url;
      link.setAttribute('download', filename);
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
      window.URL.revokeObjectURL(url); // Clean up the URL object

      return { success: true, message: 'PDF download initiated.' };
    } catch (error) {
      console.error(`Error downloading PDF for ${documentId}:`, error);
      throw error;
    }
  },

  /**
   * Gets speech audio for a document's analysis, optionally translated.
   * Corresponds to GET /analysis/<document_id>/speak?lang=<lang_code>
   * @param {string} documentId
   * @param {string} lang - The language for the speech audio.
   * @returns {string} A Blob URL for the audio.
   */
  getSpeechAudio: async (documentId, lang = 'en') => {
    try {
      const response = await api.get(`${BASE_ANALYSIS_URL}/${documentId}/speak`, {
        params: { lang },
        responseType: 'arraybuffer', // Get response as a binary blob
      });

      const blob = new Blob([response.data], { type: 'audio/mpeg' }); // Assuming MP3 audio
      const audioUrl = window.URL.createObjectURL(blob);
      return audioUrl;
    } catch (error) {
      console.error(`Error fetching speech audio for ${documentId}:`, error);
      throw error;
    }
  },
};

export default documentApiService;