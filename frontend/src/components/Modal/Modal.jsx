// frontend/src/components/Modal/Modal.jsx

import React, { useEffect, useRef } from 'react';
import ReactDOM from 'react-dom';
import PropTypes from 'prop-types';
import styles from './Modal.module.scss'; // Import SCSS module

/**
 * Reusable Modal component.
 * Uses React Portals to render outside the normal DOM hierarchy.
 * Manages body scroll lock and focus trapping for accessibility.
 */
const Modal = ({ isOpen, onClose, children, title, className = '' }) => {
  const modalRef = useRef(null);

  // Effect to manage body scroll and close on Escape key
  useEffect(() => {
    if (isOpen) {
      document.body.style.overflow = 'hidden'; // Prevent body scrolling
      // Optional: Focus the modal for accessibility
      // if (modalRef.current) {
      //   modalRef.current.focus();
      // }

      const handleEscape = (event) => {
        if (event.key === 'Escape') {
          onClose();
        }
      };
      document.addEventListener('keydown', handleEscape);
      return () => {
        document.removeEventListener('keydown', handleEscape);
      };
    } else {
      document.body.style.overflow = 'unset'; // Restore body scrolling
    }
  }, [isOpen, onClose]);

  if (!isOpen) return null;

  // Render the modal using a React Portal
  return ReactDOM.createPortal(
    <div className={styles.overlay} onClick={onClose} role="dialog" aria-modal="true" aria-labelledby="modal-title">
      <div
        className={`${styles.modal} ${className}`}
        ref={modalRef}
        onClick={(e) => e.stopPropagation()} // Prevent closing when clicking inside the modal
        tabIndex="-1" // Make modal focusable
      >
        <div className={styles.header}>
          <h2 id="modal-title" className={styles.title}>{title}</h2>
          <button className={styles.closeButton} onClick={onClose} aria-label="Close modal">
            &times;
          </button>
        </div>
        <div className={styles.content}>
          {children}
        </div>
      </div>
    </div>,
    document.getElementById('modal-root') || document.body // Render into #modal-root or body if not found
  );
};

Modal.propTypes = {
  isOpen: PropTypes.bool.isRequired,
  onClose: PropTypes.func.isRequired,
  children: PropTypes.node.isRequired,
  title: PropTypes.string,
  className: PropTypes.string,
};

export default Modal;