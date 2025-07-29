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
    const id = Date.now() + Math.random(); // Simple unique ID for message
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

// --- Optional: A simple component to display messages (you could put this in components/ or layouts/) ---
// For now, it's commented out, but this is how you'd render the messages.
/*
import styles from './MessageDisplay.module.scss'; // Assume you create this SCSS module

export const MessageDisplay = () => {
  const { messages, removeMessage } = useMessage();

  return (
    <div className={styles.messageContainer}>
      {messages.map((msg) => (
        <div
          key={msg.id}
          className={`${styles.messageItem} ${styles[msg.type]}`}
          onClick={() => removeMessage(msg.id)} // Click to dismiss
        >
          <p>{msg.text}</p>
          <button className={styles.closeButton} onClick={(e) => { e.stopPropagation(); removeMessage(msg.id); }}>
            &times;
          </button>
        </div>
      ))}
    </div>
  );
};
// Example styles for MessageDisplay.module.scss:
// .messageContainer {
//   position: fixed;
//   top: 20px;
//   right: 20px;
//   z-index: 2000;
//   display: flex;
//   flex-direction: column;
//   gap: 10px;
//   width: 300px;
// }
// .messageItem {
//   padding: 12px 15px;
//   border-radius: 5px;
//   font-size: 0.9rem;
//   font-weight: bold;
//   box-shadow: 0 2px 8px rgba(0,0,0,0.1);
//   display: flex;
//   justify-content: space-between;
//   align-items: center;
//   cursor: pointer;
// }
// .messageItem p { margin: 0; flex-grow: 1; }
// .closeButton { background: none; border: none; font-size: 1.2rem; cursor: pointer; color: inherit; }
// .success { background-color: #d4edda; color: #155724; border-left: 5px solid #28a745; }
// .error { background-color: #f8d7da; color: #721c24; border-left: 5px solid #dc3545; }
// .info { background-color: #e2f2ff; color: #004085; border-left: 5px solid #007bff; }
// .warning { background-color: #fff3cd; color: #856404; border-left: 5px solid #ffc107; }
*/