import js from "@eslint/js";
import tseslint from "@typescript-eslint/eslint-plugin";
import tsParser from "@typescript-eslint/parser";
import vuePlugin from "eslint-plugin-vue";
import vueParser from "vue-eslint-parser";
import prettier from "eslint-plugin-prettier";

// 浏览器全局变量
const browserGlobals = {
  window: "readonly",
  document: "readonly",
  navigator: "readonly",
  console: "readonly",
  setTimeout: "readonly",
  setInterval: "readonly",
  clearTimeout: "readonly",
  clearInterval: "readonly",
  fetch: "readonly",
  URL: "readonly",
  URLSearchParams: "readonly",
  FormData: "readonly",
  File: "readonly",
  FileReader: "readonly",
  Blob: "readonly",
  Image: "readonly",
  HTMLElement: "readonly",
  HTMLInputElement: "readonly",
  Event: "readonly",
  MouseEvent: "readonly",
  KeyboardEvent: "readonly",
  CustomEvent: "readonly",
  localStorage: "readonly",
  sessionStorage: "readonly",
  atob: "readonly",
  btoa: "readonly",
  AbortController: "readonly",
  Request: "readonly",
  Response: "readonly",
  Headers: "readonly",
};

// Nuxt 自动导入的全局变量
const nuxtGlobals = {
  defineNuxtConfig: "readonly",
  defineNuxtPlugin: "readonly",
  defineNuxtRouteMiddleware: "readonly",
  definePageMeta: "readonly",
  navigateTo: "readonly",
  useRoute: "readonly",
  useRouter: "readonly",
  useRuntimeConfig: "readonly",
  useState: "readonly",
  useFetch: "readonly",
  useAsyncData: "readonly",
  useLazyFetch: "readonly",
  useLazyAsyncData: "readonly",
  useHead: "readonly",
  useSeoMeta: "readonly",
  useNuxtApp: "readonly",
  ref: "readonly",
  reactive: "readonly",
  computed: "readonly",
  watch: "readonly",
  watchEffect: "readonly",
  onMounted: "readonly",
  onUnmounted: "readonly",
  onBeforeMount: "readonly",
  onBeforeUnmount: "readonly",
  nextTick: "readonly",
  defineEmits: "readonly",
  defineProps: "readonly",
  defineExpose: "readonly",
  withDefaults: "readonly",
};

// Node.js 全局变量（用于 nuxt.config.ts 等）
const nodeGlobals = {
  process: "readonly",
  __dirname: "readonly",
  __filename: "readonly",
  module: "readonly",
  require: "readonly",
  exports: "readonly",
  Buffer: "readonly",
};

export default [
  // 忽略文件
  {
    ignores: [
      "node_modules/**",
      "**/node_modules/**",
      "frontend/.nuxt/**",
      "frontend/.output/**",
      "frontend/dist/**",
      "**/*.d.ts",
      "backend/**",
    ],
  },
  // JavaScript 基础规则
  js.configs.recommended,
  // TypeScript 文件
  {
    files: ["frontend/**/*.ts", "frontend/**/*.tsx"],
    languageOptions: {
      parser: tsParser,
      parserOptions: {
        ecmaVersion: "latest",
        sourceType: "module",
      },
      globals: {
        ...browserGlobals,
        ...nuxtGlobals,
        ...nodeGlobals,
      },
    },
    plugins: {
      "@typescript-eslint": tseslint,
      prettier,
    },
    rules: {
      ...tseslint.configs.recommended.rules,
      "@typescript-eslint/no-explicit-any": "warn",
      "@typescript-eslint/no-unused-vars": [
        "warn",
        { argsIgnorePattern: "^_" },
      ],
      "prettier/prettier": "warn",
      "no-console": ["warn", { allow: ["warn", "error"] }],
      "no-debugger": "warn",
      "no-unused-vars": "off", // 使用 @typescript-eslint/no-unused-vars 代替
    },
  },
  // Vue 文件
  {
    files: ["frontend/**/*.vue"],
    languageOptions: {
      parser: vueParser,
      parserOptions: {
        parser: tsParser,
        ecmaVersion: "latest",
        sourceType: "module",
      },
      globals: {
        ...browserGlobals,
        ...nuxtGlobals,
      },
    },
    plugins: {
      vue: vuePlugin,
      "@typescript-eslint": tseslint,
      prettier,
    },
    rules: {
      ...vuePlugin.configs["vue3-recommended"].rules,
      "vue/multi-word-component-names": "off",
      "vue/no-multiple-template-root": "off",
      "vue/html-self-closing": [
        "warn",
        {
          html: {
            void: "always",
            normal: "never",
            component: "always",
          },
        },
      ],
      "@typescript-eslint/no-explicit-any": "warn",
      "prettier/prettier": "warn",
      "no-console": ["warn", { allow: ["warn", "error"] }],
      "no-unused-vars": "off", // 使用 @typescript-eslint/no-unused-vars 代替
    },
  },
];
