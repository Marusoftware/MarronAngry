import { defineConfig } from 'vite'
import { svelte } from '@sveltejs/vite-plugin-svelte'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [svelte()],
  server: {
    host: "0.0.0.0",
    port: 5000,
    proxy: {
      "/api/v1/": {
        target:"http://server:8000/",
        changeOrigin: true,
        rewrite: (path) => path.replace('/api/v1', '')
      }
    }
  }
})
