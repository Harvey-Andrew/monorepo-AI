/**
 * 项目配置
 *
 * 定义左侧菜单、路由和默认模型版本
 */

import type { ProjectConfig } from "~/types/common";

export const projects: ProjectConfig[] = [
  {
    id: "image-processing",
    name: "智图寻宝",
    icon: "MagicStick",
    route: "/apps/image-processing",
    description: "一站式智能商品识别：去噪 + 分类 + 相似推荐",
    modelVersion: "default",
  },
  {
    id: "product-classification",
    name: "商品标题分类",
    icon: "PriceTag",
    route: "/apps/product-classification",
    description: "基于 BERT 的中文商品标题智能分类，支持 30 种类别",
    modelVersion: "default",
  },
  {
    id: "ai-news",
    name: "智选新闻",
    icon: "Document",
    route: "/apps/ai-news",
    description: "基于 BART 的中文新闻智能分类与摘要生成",
    modelVersion: "default",
  },
  {
    id: "address-alignment",
    name: "地址对齐",
    icon: "Location",
    route: "/apps/address-alignment",
    description: "基于 BERT 的中文地址智能解析，支持 7 类实体提取",
    modelVersion: "default",
  },
  {
    id: "chat",
    name: "AI 助手",
    icon: "ChatDotRound",
    route: "/apps/chat",
    description: "基于 Gemini 的智能对话助手，支持流式响应",
    modelVersion: "default",
  },
];

export default projects;
