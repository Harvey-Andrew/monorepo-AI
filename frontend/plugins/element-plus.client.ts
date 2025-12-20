/**
 * Element Plus 插件配置
 *
 * - 全局注册 Element Plus 组件
 * - 注册图标组件
 * - 配置中文语言包
 */
import ElementPlus from "element-plus";
import zhCn from "element-plus/es/locale/lang/zh-cn";
import * as ElementPlusIconsVue from "@element-plus/icons-vue";
import "element-plus/dist/index.css";

export default defineNuxtPlugin((nuxtApp) => {
  // 注册 Element Plus
  nuxtApp.vueApp.use(ElementPlus, {
    locale: zhCn,
  });

  // 全局注册所有图标
  for (const [key, component] of Object.entries(ElementPlusIconsVue)) {
    nuxtApp.vueApp.component(key, component);
  }
});
