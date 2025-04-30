// vite.config.js
import { defineConfig } from 'vite';
import solid from 'vite-plugin-solid';

export default defineConfig({
  plugins: [solid()],
  server: {
    host: true, // or use '0.0.0.0'
    port: 3000  // or any port you want
  }
});
