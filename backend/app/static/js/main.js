// backend/app/static/js/main.js

// This file is for very basic, non-framework-specific JavaScript
// that might be needed by Flask-rendered templates (e.g., error pages).

// Example: A simple script to hide flash messages after a few seconds
document.addEventListener('DOMContentLoaded', () => {
    const flashMessages = document.querySelectorAll('.flashes li');
    flashMessages.forEach(msg => {
        setTimeout(() => {
            msg.style.opacity = '0';
            msg.style.transition = 'opacity 0.5s ease-out';
            setTimeout(() => msg.remove(), 500); // Remove after transition
        }, 5000); // Message visible for 5 seconds
    });
});

// You might add functions here for:
// - Simple form validation (though preferable to use JS frameworks or server-side)
// - Basic UI toggles
// - Sending simple AJAX requests not handled by the main React app