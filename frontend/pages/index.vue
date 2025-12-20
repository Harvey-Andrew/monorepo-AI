<template>
  <div class="home-page">
    <header class="page-header">
      <div class="brand">
        <h1 class="brand-title">My Local AI Hub</h1>
        <p class="brand-subtitle">本地 AI 推理服务</p>
      </div>
    </header>

    <main class="main-content">
      <h2 class="section-title">功能模块</h2>
      <div class="project-grid">
        <NuxtLink
          v-for="project in projects"
          :key="project.id"
          :to="project.route"
          class="project-card"
        >
          <el-icon class="project-icon" :size="32">
            <component :is="getIcon(project.icon)" />
          </el-icon>
          <div class="project-info">
            <h3 class="project-name">{{ project.name }}</h3>
            <p class="project-desc">{{ project.description }}</p>
          </div>
          <el-icon class="project-arrow">
            <ArrowRight />
          </el-icon>
        </NuxtLink>
      </div>
    </main>
  </div>
</template>

<script setup lang="ts">
import {
  Brush,
  Histogram,
  Search,
  ArrowRight,
  MagicStick,
} from "@element-plus/icons-vue";
import { projects } from "~/constants/projects";

const iconMap: Record<string, any> = {
  Brush,
  Histogram,
  Search,
  MagicStick,
};

const getIcon = (name: string) => iconMap[name] || Brush;

useSeoMeta({
  title: "My Local AI Hub - 本地 AI 推理服务",
  description: "图像去噪、商品分类、相似检索等 AI 功能",
});
</script>

<style lang="scss" scoped>
.home-page {
  max-width: 1200px;
  margin: 0 auto;
  padding: 24px;
}

.page-header {
  text-align: center;
  margin-bottom: 48px;
  padding: 32px;
  background: linear-gradient(
    135deg,
    var(--el-color-primary-light-7),
    var(--el-color-primary-light-9)
  );
  border-radius: 16px;
}

.brand-title {
  font-size: 32px;
  font-weight: 700;
  margin: 0;
  color: var(--el-color-primary);
}

.brand-subtitle {
  font-size: 16px;
  color: var(--el-text-color-secondary);
  margin: 8px 0 0;
}

.section-title {
  font-size: 20px;
  font-weight: 600;
  margin: 0 0 24px;
  color: var(--el-text-color-primary);
}

.project-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 16px;
}

.project-card {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 20px;
  background: var(--el-bg-color);
  border: 1px solid var(--el-border-color);
  border-radius: 12px;
  text-decoration: none;
  transition: all 0.3s ease;

  &:hover {
    border-color: var(--el-color-primary);
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
    transform: translateY(-2px);

    .project-arrow {
      transform: translateX(4px);
    }
  }
}

.project-icon {
  flex-shrink: 0;
  color: var(--el-color-primary);
  background: var(--el-color-primary-light-9);
  padding: 12px;
  border-radius: 10px;
}

.project-info {
  flex: 1;
  min-width: 0;
}

.project-name {
  font-size: 16px;
  font-weight: 600;
  margin: 0;
  color: var(--el-text-color-primary);
}

.project-desc {
  font-size: 13px;
  color: var(--el-text-color-secondary);
  margin: 4px 0 0;
}

.project-arrow {
  flex-shrink: 0;
  color: var(--el-text-color-placeholder);
  transition: transform 0.3s ease;
}
</style>
