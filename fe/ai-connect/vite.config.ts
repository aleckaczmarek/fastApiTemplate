import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react()],
  server:{
    open:'/',
    port:3000,
    proxy:{ 
      '/api/ai/ask': {
        target: 'http://0.0.0.0:8090',
        changeOrigin: true,
        secure:false
      }
    }
  }
})
