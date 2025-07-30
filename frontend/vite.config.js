// frontend/vite.config.js
import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';
import svgr from 'vite-plugin-svgr'; // Import svgr
import path from 'path';

export default defineConfig({
  plugins: [
    react(),
    svgr({ // Configure svgr to ensure it targets the right files
      include: '**/*.svg?react', // This tells svgr to process files ending with .svg?react
    }),
  ],
  resolve: {
    alias: {
      '~styles': path.resolve(__dirname, 'src/styles'),
      // Add an alias for assets too for clarity, though relative path should work
      '~assets': path.resolve(__dirname, 'src/assets'), // Add this for consistency
    },
  },
  // ... other config (css, etc.)
});
