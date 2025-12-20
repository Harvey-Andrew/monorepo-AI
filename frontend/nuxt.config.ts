// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
  devtools: { enabled: true },
  ssr: true,

  // 运行时配置
  runtimeConfig: {
    // 仅服务端可访问 - Python 后端地址
    pythonApiBase: process.env.PYTHON_API_BASE || "http://127.0.0.1:9000",
  },

  // CSS 配置
  css: ["~/assets/styles/main.scss"],

  // Nitro 开发代理
  nitro: {
    devProxy: {
      "/api": {
        target: "http://127.0.0.1:9000/api",
        changeOrigin: true,
      },
      "/storage": {
        target: "http://127.0.0.1:9000/storage",
        changeOrigin: true,
      },
    },
  },

  // Vite 配置
  vite: {
    optimizeDeps: {
      include: ["element-plus"],
    },
    css: {
      preprocessorOptions: {
        scss: {
          silenceDeprecations: ["import"],
          additionalData: `@import "~/assets/styles/_variables.scss";`,
        },
      },
    },
  },

  // 应用元信息
  app: {
    head: {
      title: "My Local AI Hub",
      meta: [
        { charset: "utf-8" },
        { name: "viewport", content: "width=device-width, initial-scale=1" },
        {
          name: "description",
          content: "本地 AI 推理服务 - 图像去噪、商品分类、相似检索",
        },
      ],
      htmlAttrs: { lang: "zh-CN" },
      // 关键加载样式内联，避免样式闪烁
      style: [
        {
          innerHTML: `
            .global-loading {
              position: fixed;
              top: 0;
              left: 0;
              right: 0;
              bottom: 0;
              background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
              display: flex;
              align-items: center;
              justify-content: center;
              z-index: 9999;
            }
            .global-loading .loading-content {
              display: flex;
              flex-direction: column;
              align-items: center;
              gap: 24px;
            }
            .global-loading .loading-logo {
              font-size: 64px;
              animation: pulse 2s ease-in-out infinite;
            }
            .global-loading .loading-spinner {
              width: 40px;
              height: 40px;
              border: 3px solid rgba(255, 255, 255, 0.3);
              border-top-color: white;
              border-radius: 50%;
              animation: spin 1s linear infinite;
            }
            .global-loading .loading-text {
              color: white;
              font-size: 16px;
              font-weight: 500;
              letter-spacing: 2px;
            }
            @keyframes spin {
              to { transform: rotate(360deg); }
            }
            @keyframes pulse {
              0%, 100% { transform: scale(1); opacity: 1; }
              50% { transform: scale(1.05); opacity: 0.8; }
            }
            .fade-enter-active, .fade-leave-active {
              transition: opacity 0.5s ease;
            }
            .fade-enter-from, .fade-leave-to {
              opacity: 0;
            }
          `,
        },
      ],
    },
  },

  // 兼容性日期
  compatibilityDate: "2024-12-01",
});
