# MinerU 项目规范

## 前后端网络架构（不可偏离）

- 前端 `API_BASE` **必须**为空字符串 `''`（相对路径），**禁止**硬编码任何主机名或端口号
- `vite.config.js` 必须配置 proxy 将 API 请求代转到 `http://127.0.0.1:8267`
- `vite.config.js` 必须设置 `server.host: '0.0.0.0'`
- 后端绑定 `0.0.0.0:8267`，但**不直接对外暴露**，所有外部请求通过 Vite proxy 代转

## 前端开发

- 框架: Vue 3 + Vite
- 端口: 3000
- UI 组件在 `frontend/src/App.vue`（单文件应用）
- 构建: `npm run build`，开发: `npm run dev`
- 所有后端 API 调用使用相对路径（如 `/options`、`/upload`），不拼接主机名

## 后端开发

- 框架: FastAPI + uvicorn
- 端口: 8267
- 入口: `backend/main.py`
- CORS: 允许所有来源
