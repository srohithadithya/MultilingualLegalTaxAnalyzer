// frontend/src/store/messageStore.js

import React, { createContext, useContext, useState, useCallback } from 'react';
import PropTypes from 'prop-types';

// Create the MessageContext
export const MessageContext = createContext(null);

/**
 * MessageProvider component manages a global list of messages.
 * Components can add or remove messages.
 */
export const MessageProvider = ({ children }) => {
  const [messages, setMessages] = useState([]); // Format: [{ id: 'uuid', type: 'success'/'error'/'info', text: '...' }]

  /**
   * Adds a new message to the global list.
   * @param {string} text - The message text.
   * @param {'success'|'error'|'info'|'warning'} type - The type of message.
   * @param {number} [duration=5000] - Duration in ms after which the message auto-removes (0 for permanent).
   */
  const addMessage = useCallback((text, type = 'info', duration = 5000) => {
    const id = Date.now() + Math.random(); // Simple unique ID
    const newMessage = { id, text, type };
    setMessages((prevMessages) => [...prevMessages, newMessage]);

    // Automatically remove message after a duration
    if (duration > 0) {
      setTimeout(() => {
        removeMessage(id);
      }, duration);
    }
  }, []);

  /**
   * Removes a specific message by its ID.
   * @param {number} id - The ID of the message to remove.
   */
  const removeMessage = useCallback((id) => {
    setMessages((prevMessages) => prevMessages.filter((msg) => msg.id !== id));
  }, []);

  /**
   * Clears all current messages.
   */
  const clearAllMessages = useCallback(() => {
    setMessages([]);
  }, []);

  const contextValue = {
    messages,
    addMessage,
    removeMessage,
    clearAllMessages,
  };

  return (
    <MessageContext.Provider value={contextValue}>
      {children}
    </MessageContext.Provider>
  );
};

MessageProvider.propTypes = {
  children: PropTypes.node.isRequired,
};

/**
 * Custom hook to consume the MessageContext.
 * @returns {{messages: Array, addMessage: Function, removeMessage: Function, clearAllMessages: Function}}
 */
export const useMessage = () => {
  const context = useContext(MessageContext);
  if (context === undefined) {
    throw new Error('useMessage must be used within a MessageProvider');
  }
  return context;
};
