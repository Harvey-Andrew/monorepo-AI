/**
 * 项目配置
 *
 * 定义左侧菜单、路由和默认模型版本
 */

export interface ProjectConfig {
  /** 项目唯一标识 */
  id: string;
  /** 显示名称 */
  name: string;
  /** 图标 (Element Plus 图标名) */
  icon: string;
  /** 路由路径 */
  route: string;
  /** 描述 */
  description: string;
  /** 默认模型版本 */
  modelVersion?: string;
}

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
