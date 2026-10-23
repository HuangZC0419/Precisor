import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

export default defineConfig({
  plugins: [vue()],
  server: {
    host: '0.0.0.0',
    port: 3000,
    proxy: {
      '/': {
        target: 'http://127.0.0.1:8267',
        bypass(req) {
          const url = req.url || ''
          // Vite 内部路径和前端资源不代理，由 Vite 正常处理
          if (
            url === '/' ||
            url.startsWith('/@') ||
            url.startsWith('/src') ||
            url.startsWith('/node_modules') ||
            url.startsWith('/assets') ||
            url.startsWith('/favicon')
          ) {
            return url
          }
          // 其余请求（/options, /upload, /result/* 等）代理到后端
        }
      }
    }
  }
})
