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
];

export default projects;
