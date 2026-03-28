<template>
  <div class="app-page">
    <!-- 页面头部 -->
    <header class="page-header">
      <NuxtLink to="/" class="back-link">
        <el-icon><ArrowLeft /></el-icon>
        返回首页
      </NuxtLink>
      <h1 class="page-title">📰 智选新闻</h1>
      <p class="page-desc">
        基于 BART 的中文新闻智能分类与摘要生成，支持 7 类新闻识别
      </p>
    </header>

    <!-- 主内容区 -->
    <main class="main-content">
      <!-- 输入区域 -->
      <section class="input-section glass-card">
        <h2 class="section-title">输入新闻内容</h2>
        <el-input
          v-model="inputText"
          type="textarea"
          :rows="8"
          placeholder="请输入需要分析的新闻文本...（建议长度100-500字）"
          :disabled="isLoading"
        />
        <div class="action-bar">
          <el-button
            type="primary"
            size="large"
            :loading="isLoading"
            :disabled="!inputText.trim()"
            @click="handleAnalyze"
          >
            {{ isLoading ? "分析中..." : "智能分析" }}
          </el-button>
          <el-button size="large" :disabled="isLoading" @click="handleClear">
            清除
          </el-button>
        </div>
      </section>

      <!-- 结果展示 -->
      <section v-if="category || summary" class="result-section glass-card">
        <h2 class="section-title">分析结果</h2>
        <div class="result-content">
          <!-- 分类结果 -->
          <div class="result-item">
            <span class="result-label">新闻分类：</span>
            <el-tag
              type="success"
              size="large"
              effect="dark"
              class="category-tag"
            >
              {{ category || "待分析" }}
            </el-tag>
          </div>
          <!-- 摘要结果 -->
          <div class="result-item summary-item">
            <span class="result-label">智能摘要：</span>
            <div class="summary-text">
              {{ summary || "待生成" }}
            </div>
          </div>
        </div>
      </section>

      <!-- 历史记录 -->
      <section v-if="history.length > 0" class="history-section glass-card">
        <div class="section-header">
          <h2 class="section-title">历史记录</h2>
          <el-button text type="danger" size="small" @click="clearHistory">
            清除历史
          </el-button>
        </div>
        <el-table :data="history" stripe style="width: 100%">
          <el-table-column prop="text" label="新闻内容" min-width="200">
            <template #default="{ row }">
              <el-tooltip :content="row.text" placement="top" :show-after="500">
                <span class="text-ellipsis">{{ row.text }}</span>
              </el-tooltip>
            </template>
          </el-table-column>
          <el-table-column prop="category" label="分类" width="100">
            <template #default="{ row }">
              <el-tag size="small">{{ row.category }}</el-tag>
            </template>
          </el-table-column>
          <el-table-column prop="summary" label="摘要" min-width="150">
            <template #default="{ row }">
              <el-tooltip
                :content="row.summary"
                placement="top"
                :show-after="500"
              >
                <span class="text-ellipsis">{{ row.summary }}</span>
              </el-tooltip>
            </template>
          </el-table-column>
          <el-table-column label="时间" width="80">
            <template #default="{ row }">
              {{ formatTime(row.timestamp) }}
            </template>
          </el-table-column>
        </el-table>
      </section>

      <!-- 支持的分类类别 -->
      <section class="categories-section glass-card">
        <h2 class="section-title">支持的新闻类别</h2>
        <div class="categories-grid">
          <el-tag
            v-for="cat in supportedCategories"
            :key="cat.name"
            :type="cat.type"
            class="category-item"
          >
            {{ cat.icon }} {{ cat.name }}
          </el-tag>
        </div>
      </section>
    </main>
  </div>
</template>

<script setup lang="ts">
import { watch } from "vue";
import { ArrowLeft } from "@element-plus/icons-vue";
import { ElMessage } from "element-plus";
import { useAiNews } from "~/composables/useAiNews";

// 使用 AI News Composable
const {
  inputText,
  category,
  summary,
  isLoading,
  error,
  history,
  analyze,
  clearResult,
  clearHistory,
  clearError,
} = useAiNews();

// 支持的分类类别
const supportedCategories = [
  { name: "财经", icon: "💰", type: "warning" as const },
  { name: "社会", icon: "🏛️", type: "info" as const },
  { name: "教育", icon: "📚", type: "success" as const },
  { name: "科技", icon: "🔬", type: "primary" as const },
  { name: "时政", icon: "🏢", type: "danger" as const },
  { name: "体育", icon: "⚽", type: "warning" as const },
  { name: "游戏", icon: "🎮", type: "success" as const },
];

// 处理分析
async function handleAnalyze() {
  try {
    await analyze();
    ElMessage.success("分析完成！");
  } catch {
    // 错误已在 composable 中处理
  }
}

// 处理清除
function handleClear() {
  inputText.value = "";
  clearResult();
}

// 格式化时间
function formatTime(date: Date) {
  return date.toLocaleTimeString("zh-CN", {
    hour: "2-digit",
    minute: "2-digit",
  });
}

// 监听错误
watch(error, (newError) => {
  if (newError) {
    ElMessage.error(newError);
    clearError();
  }
});

// SEO 元信息
useSeoMeta({
  title: "智选新闻 - My Local AI Hub",
  description: "基于 BART 的中文新闻智能分类与摘要生成系统，支持 7 类新闻识别",
  ogTitle: "智选新闻 - My Local AI Hub",
  ogDescription: "基于 BART 的中文新闻智能分类与摘要生成系统",
  ogType: "website",
});
</script>

<style lang="scss" scoped>
.app-page {
  max-width: 900px;
  margin: 0 auto;
  padding: 24px;
}

.page-header {
  margin-bottom: 32px;
}

.back-link {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  font-size: 14px;
  color: var(--el-text-color-secondary);
  text-decoration: none;
  margin-bottom: 16px;
  transition: color 0.25s ease;

  &:hover {
    color: var(--el-color-primary);
  }
}

.page-title {
  font-size: 32px;
  font-weight: 700;
  margin: 0;
  background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
  background-clip: text;
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

.page-desc {
  font-size: 14px;
  color: var(--el-text-color-secondary);
  margin: 8px 0 0;
}

.glass-card {
  background: rgba(255, 255, 255, 0.8);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.3);
  border-radius: 16px;
  padding: 24px;
  margin-bottom: 24px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.08);
}

.section-title {
  font-size: 18px;
  font-weight: 600;
  margin: 0 0 16px;
  color: var(--el-text-color-primary);
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;

  .section-title {
    margin: 0;
  }
}

.action-bar {
  display: flex;
  gap: 12px;
  margin-top: 16px;
}

.result-content {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.result-item {
  display: flex;
  align-items: flex-start;
  gap: 12px;
}

.result-label {
  font-weight: 500;
  color: var(--el-text-color-regular);
  white-space: nowrap;
  min-width: 80px;
}

.category-tag {
  font-size: 16px;
  padding: 8px 20px;
  border-radius: 6px;
}

.summary-item {
  flex-direction: column;
  gap: 8px;
}

.summary-text {
  background: linear-gradient(135deg, #f5f7fa 0%, #e4e8ec 100%);
  border-radius: 8px;
  padding: 16px;
  font-size: 15px;
  line-height: 1.8;
  color: var(--el-text-color-primary);
}

.text-ellipsis {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
  text-overflow: ellipsis;
}

.categories-grid {
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
}

.category-item {
  font-size: 14px;
  padding: 8px 16px;
}

/* 暗色模式适配 */
:root.dark .glass-card {
  background: rgba(30, 30, 30, 0.8);
  border-color: rgba(255, 255, 255, 0.1);
}

:root.dark .summary-text {
  background: linear-gradient(135deg, #2d2d2d 0%, #1a1a1a 100%);
}
</style>
