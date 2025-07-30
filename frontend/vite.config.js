// frontend/vite.config.js
import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';
import path from 'path'; // Import 'path' module

export default defineConfig({
  plugins: [react()],
  resolve: {
    alias: {
      // Define an alias for your src/styles folder
      '~styles': path.resolve(__dirname, 'src/styles'),
    },
  },
  css: {
    preprocessorOptions: {
      scss: {
        // Optional: Automatically import variables/mixins into all SCSS files
        // This avoids having to @use them in every component's SCSS file.
        // Be careful, this can increase build times if not managed well.
        // For now, we will stick to explicit @use statements.
        // You can add global data like:
        // additionalData: `@use "~/styles/variables" as *; @use "~/styles/mixins" as *;`
      },
    },
  },
});
