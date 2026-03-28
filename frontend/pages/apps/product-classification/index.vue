<template>
  <div class="app-page">
    <!-- 页面头部 -->
    <header class="page-header">
      <NuxtLink to="/" class="back-link">
        <el-icon><ArrowLeft /></el-icon>
        返回首页
      </NuxtLink>
      <h1 class="page-title">🏷️ 商品标题分类</h1>
      <p class="page-desc">
        基于 BERT 的中文商品标题智能分类，支持 30 种商品类别识别
      </p>
    </header>

    <!-- 主内容区 -->
    <main class="main-content">
      <!-- 输入区域 -->
      <section class="input-section glass-card">
        <h2 class="section-title">输入商品标题</h2>
        <el-input
          v-model="inputText"
          type="textarea"
          :rows="3"
          placeholder="请输入商品标题，例如：好奇心钻装纸尿裤L40片9-14kg"
          :disabled="isLoading"
        />
        <div class="action-bar">
          <el-button
            type="primary"
            size="large"
            :loading="isLoading"
            :disabled="!inputText.trim()"
            @click="handleClassify"
          >
            {{ isLoading ? "分类中..." : "开始分类" }}
          </el-button>
          <el-button size="large" :disabled="isLoading" @click="handleClear">
            清除
          </el-button>
        </div>
      </section>

      <!-- 结果展示 -->
      <section v-if="category" class="result-section glass-card">
        <h2 class="section-title">分类结果</h2>
        <div class="result-display">
          <el-tag
            type="success"
            size="large"
            effect="dark"
            class="category-tag"
          >
            {{ category }}
          </el-tag>
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
          <el-table-column prop="text" label="商品标题" min-width="200" />
          <el-table-column prop="category" label="分类" width="120">
            <template #default="{ row }">
              <el-tag size="small">{{ row.category }}</el-tag>
            </template>
          </el-table-column>
          <el-table-column label="时间" width="100">
            <template #default="{ row }">
              {{ formatTime(row.timestamp) }}
            </template>
          </el-table-column>
        </el-table>
      </section>

      <!-- 支持的分类类别 -->
      <section class="categories-section glass-card">
        <h2 class="section-title">支持的分类类别</h2>
        <div class="categories-grid">
          <el-tag
            v-for="cat in supportedCategories"
            :key="cat"
            class="category-item"
          >
            {{ cat }}
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
import { useProductClassification } from "~/composables/useProductClassification";

// 使用商品分类 Composable
const {
  inputText,
  category,
  isLoading,
  error,
  history,
  classify,
  clearResult,
  clearHistory,
  clearError,
} = useProductClassification();

// 支持的分类类别
const supportedCategories = [
  "3C数码",
  "个护",
  "书籍",
  "乳品",
  "休闲食品",
  "健康",
  "健康食品",
  "办公",
  "宠物",
  "家居",
  "家电",
  "服饰内衣",
  "母婴",
  "水产",
  "水果",
  "汽车用品",
  "清洁",
  "玩具",
  "礼品",
  "粮油速食",
  "美妆",
  "肉禽蛋",
  "蔬菜",
  "运动",
  "酒饮冲调",
  "钟表配饰",
  "鞋靴箱包",
  "餐饮",
  "香烟",
  "鲜花绿植",
];

// 处理分类
async function handleClassify() {
  try {
    await classify();
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
  title: "商品标题分类 - My Local AI Hub",
  description: "基于 BERT 的中文商品标题智能分类系统，支持 30 种商品类别识别",
  ogTitle: "商品标题分类 - My Local AI Hub",
  ogDescription: "基于 BERT 的中文商品标题智能分类系统",
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
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
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

.result-display {
  display: flex;
  justify-content: center;
  padding: 32px;
}

.category-tag {
  font-size: 24px;
  padding: 12px 32px;
  border-radius: 8px;
}

.categories-grid {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.category-item {
  font-size: 13px;
}

/* 暗色模式适配 */
:root.dark .glass-card {
  background: rgba(30, 30, 30, 0.8);
  border-color: rgba(255, 255, 255, 0.1);
}
</style>
