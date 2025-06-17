import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  define: {
    'process.env': {}  // ← empêche erreurs si jamais process.env est appelé
  },
  server: {
    port: 3000,
  },
})
