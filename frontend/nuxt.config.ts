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
    },
  },

  // 兼容性日期
  compatibilityDate: "2024-12-01",
});
