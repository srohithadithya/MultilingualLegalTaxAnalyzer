// frontend/src/features/document-analysis/hooks/useDocumentAnalysis.js

import { useState, useEffect, useCallback } from 'react';
import analysisService from '../analysisService'; // Feature-specific service
import { useAuth } from '../../auth/hooks/useAuth'; // To get current user info if needed

/**
 * Custom hook to manage document analysis operations (upload, fetch, actions).
 */
export const useDocumentAnalysis = () => {
  const { isAuthenticated, user } = useAuth(); // Get auth state
  const [documents, setDocuments] = useState([]); // List of previously analyzed documents
  const [currentAnalysis, setCurrentAnalysis] = useState(null); // Detailed analysis for one document
  const [loading, setLoading] = useState(false);
  const [uploading, setUploading] = useState(false);
  const [error, setError] = useState(null);
  const [message, setMessage] = useState(null); // Success/info messages

  // --- Fetch Previous Analyses ---
  const fetchPreviousAnalyses = useCallback(async () => {
    if (!isAuthenticated || !user) {
      setDocuments([]);
      return;
    }
    setLoading(true);
    setError(null);
    try {
      const data = await analysisService.getPreviousAnalyses();
      setDocuments(data.documents || []);
      setMessage(data.message || 'Previous analyses loaded.');
    } catch (err) {
      setError(err.response?.data?.message || 'Failed to load previous analyses.');
      console.error('Fetch previous analyses error:', err);
      setDocuments([]);
    } finally {
      setLoading(false);
    }
  }, [isAuthenticated, user]);

  useEffect(() => {
    fetchPreviousAnalyses();
  }, [fetchPreviousAnalyses]); // Fetch on mount and when auth state changes

  // --- Upload Document ---
  const uploadDocument = useCallback(async (file) => {
    if (!isAuthenticated || !user) {
      setError('You must be logged in to upload documents.');
      return null;
    }
    setUploading(true);
    setError(null);
    setMessage(null);
    try {
      const response = await analysisService.uploadAndAnalyzeDocument(file);
      setMessage(response.message || 'Document uploaded and analysis started.');
      // After successful upload, refresh the list of documents
      fetchPreviousAnalyses();
      // If the response includes the new analysis, return it for immediate display
      return response.analysis_result;
    } catch (err) {
      setError(err.response?.data?.message || 'Failed to upload and analyze document.');
      console.error('Upload document error:', err);
      return null;
    } finally {
      setUploading(false);
    }
  }, [isAuthenticated, user, fetchPreviousAnalyses]);


  // --- Fetch Detailed Analysis ---
  const fetchDetailedAnalysis = useCallback(async (documentId) => {
    if (!isAuthenticated || !user) {
      setError('You must be logged in to view analysis.');
      return;
    }
    setLoading(true);
    setError(null);
    try {
      const data = await analysisService.getDetailedAnalysis(documentId);
      setCurrentAnalysis(data);
      setMessage(data.message || 'Detailed analysis loaded.');
    } catch (err) {
      setError(err.response?.data?.message || `Failed to load analysis for document ${documentId}.`);
      console.error(`Fetch detailed analysis for ${documentId} error:`, err);
      setCurrentAnalysis(null);
    } finally {
      setLoading(false);
    }
  }, [isAuthenticated, user]);


  // --- Document Actions (PDF Download, Speech) ---
  const downloadPdf = useCallback(async (documentId, lang) => {
    setLoading(true); // Can use a separate loading state for actions if more granular control is needed
    setError(null);
    setMessage(null);
    try {
      await analysisService.downloadAnalysisPdf(documentId, lang);
      setMessage('PDF download initiated successfully.');
    } catch (err) {
      setError(err.response?.data?.message || 'Failed to download PDF report.');
      console.error('Download PDF error:', err);
    } finally {
      setLoading(false);
    }
  }, []);

  const playSpeech = useCallback(async (documentId, lang) => {
    setLoading(true);
    setError(null);
    setMessage(null);
    try {
      const audioUrl = await analysisService.getAnalysisSpeech(documentId, lang);
      if (audioUrl) {
        const audio = new Audio(audioUrl);
        audio.play();
        setMessage('Playing analysis audio.');
      } else {
        setMessage('No audio content received.');
      }
    } catch (err) {
      setError(err.response?.data?.message || 'Failed to play speech audio.');
      console.error('Play speech error:', err);
    } finally {
      setLoading(false);
    }
  }, []);

  return {
    documents,
    currentAnalysis,
    loading,
    uploading,
    error,
    message,
    fetchPreviousAnalyses,
    uploadDocument,
    fetchDetailedAnalysis,
    downloadPdf,
    playSpeech,
    clearMessages: () => { setError(null); setMessage(null); },
  };
};

export default useDocumentAnalysis;