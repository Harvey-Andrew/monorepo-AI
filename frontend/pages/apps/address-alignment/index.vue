<template>
  <div class="app-page">
    <!-- 页面头部 -->
    <header class="page-header">
      <NuxtLink to="/" class="back-link">
        <el-icon><ArrowLeft /></el-icon>
        返回首页
      </NuxtLink>
      <h1 class="page-title">📍 地址对齐</h1>
      <p class="page-desc">
        基于 BERT 的中文地址智能解析，支持省市区街道等 7 类实体提取
      </p>
    </header>

    <!-- 主内容区 -->
    <main class="main-content">
      <!-- 输入区域 -->
      <section class="input-section glass-card">
        <h2 class="section-title">输入地址</h2>
        <el-input
          v-model="inputText"
          type="textarea"
          :rows="3"
          placeholder="请输入完整地址，例如：浙江省杭州市余杭区葛墩路27号楼傅婷15830444519"
          :disabled="isLoading"
        />
        <div class="action-bar">
          <el-button
            type="primary"
            size="large"
            :loading="isLoading"
            :disabled="!inputText.trim()"
            @click="handleAlign"
          >
            {{ isLoading ? "解析中..." : "智能解析" }}
          </el-button>
          <el-button size="large" :disabled="isLoading" @click="handleClear">
            清除
          </el-button>
        </div>
      </section>

      <!-- 结果展示 -->
      <section v-if="result" class="result-section glass-card">
        <h2 class="section-title">解析结果</h2>
        <div class="result-grid">
          <div v-for="item in resultItems" :key="item.key" class="result-item">
            <span class="result-label">{{ item.label }}</span>
            <span class="result-value" :class="{ empty: !item.value }">
              {{ item.value || "未识别" }}
            </span>
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
          <el-table-column prop="text" label="原始地址" min-width="200">
            <template #default="{ row }">
              <el-tooltip :content="row.text" placement="top" :show-after="500">
                <span class="text-ellipsis">{{ row.text }}</span>
              </el-tooltip>
            </template>
          </el-table-column>
          <el-table-column label="省份" width="80">
            <template #default="{ row }">
              {{ row.prov || "-" }}
            </template>
          </el-table-column>
          <el-table-column label="城市" width="80">
            <template #default="{ row }">
              {{ row.city || "-" }}
            </template>
          </el-table-column>
          <el-table-column label="区县" width="80">
            <template #default="{ row }">
              {{ row.district || "-" }}
            </template>
          </el-table-column>
          <el-table-column label="时间" width="80">
            <template #default="{ row }">
              {{ formatTime(row.timestamp) }}
            </template>
          </el-table-column>
        </el-table>
      </section>

      <!-- 支持的实体类型 -->
      <section class="entities-section glass-card">
        <h2 class="section-title">支持的实体类型</h2>
        <div class="entities-grid">
          <el-tag
            v-for="entity in supportedEntities"
            :key="entity.name"
            :type="entity.type"
            class="entity-item"
          >
            {{ entity.icon }} {{ entity.name }}
          </el-tag>
        </div>
      </section>
    </main>
  </div>
</template>

<script setup lang="ts">
import { watch, computed } from "vue";
import { ArrowLeft } from "@element-plus/icons-vue";
import { ElMessage } from "element-plus";
import { useAddressAlignment } from "~/composables/useAddressAlignment";

// 使用 Address Alignment Composable
const {
  inputText,
  result,
  isLoading,
  error,
  history,
  align,
  clearResult,
  clearHistory,
  clearError,
} = useAddressAlignment();

// 支持的实体类型
const supportedEntities = [
  { name: "省份", icon: "🏛️", type: "primary" as const },
  { name: "城市", icon: "🏙️", type: "success" as const },
  { name: "区县", icon: "🏘️", type: "warning" as const },
  { name: "街道", icon: "🛣️", type: "info" as const },
  { name: "详细地址", icon: "📮", type: "danger" as const },
  { name: "姓名", icon: "👤", type: "primary" as const },
  { name: "电话", icon: "📞", type: "success" as const },
];

// 结果项
const resultItems = computed(() => {
  if (!result.value) return [];
  return [
    { key: "prov", label: "省份", value: result.value.prov },
    { key: "city", label: "城市", value: result.value.city },
    { key: "district", label: "区县", value: result.value.district },
    { key: "town", label: "街道", value: result.value.town },
    { key: "detail", label: "详细地址", value: result.value.detail },
    { key: "name", label: "姓名", value: result.value.name },
    { key: "phone", label: "电话", value: result.value.phone },
  ];
});

// 处理解析
async function handleAlign() {
  try {
    await align();
    ElMessage.success("地址解析成功！");
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
  title: "地址对齐 - My Local AI Hub",
  description:
    "基于 BERT 的中文地址智能解析系统，支持省市区街道等 7 类实体提取",
  ogTitle: "地址对齐 - My Local AI Hub",
  ogDescription: "基于 BERT 的中文地址智能解析系统",
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
  background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
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

.result-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 16px;
}

.result-item {
  display: flex;
  flex-direction: column;
  gap: 4px;
  padding: 12px;
  background: linear-gradient(135deg, #f5f7fa 0%, #e4e8ec 100%);
  border-radius: 8px;
}

.result-label {
  font-size: 12px;
  color: var(--el-text-color-secondary);
}

.result-value {
  font-size: 16px;
  font-weight: 500;
  color: var(--el-text-color-primary);

  &.empty {
    color: var(--el-text-color-placeholder);
    font-style: italic;
  }
}

.text-ellipsis {
  display: -webkit-box;
  -webkit-line-clamp: 1;
  -webkit-box-orient: vertical;
  overflow: hidden;
  text-overflow: ellipsis;
}

.entities-grid {
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
}

.entity-item {
  font-size: 14px;
  padding: 8px 16px;
}

/* 暗色模式适配 */
:root.dark .glass-card {
  background: rgba(30, 30, 30, 0.8);
  border-color: rgba(255, 255, 255, 0.1);
}

:root.dark .result-item {
  background: linear-gradient(135deg, #2d2d2d 0%, #1a1a1a 100%);
}
</style>
