import { defineConfig } from 'vite'
import { svelte } from '@sveltejs/vite-plugin-svelte'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [svelte()],
  server: {
    port: 5000,
    proxy: {
      "/api/v1/": {
        target:"http://localhost:8000/",
        changeOrigin: true,
        rewrite: (path) => path.replace('/api/v1', '')
      }
    }
  }
})
