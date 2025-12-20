<template>
  <div class="similar-image-grid">
    <template v-if="images.length > 0">
      <div
        v-for="(image, index) in images"
        :key="index"
        class="similar-item"
        @click="handlePreview(index)"
      >
        <el-image
          :src="getImageUrl(image)"
          :alt="`相似商品 ${index + 1}`"
          fit="cover"
          lazy
          class="similar-image"
        >
          <template #placeholder>
            <div class="image-loading">
              <el-icon class="is-loading"><Loading /></el-icon>
            </div>
          </template>
          <template #error>
            <div class="image-error">
              <el-icon><PictureFilled /></el-icon>
            </div>
          </template>
        </el-image>
        <div class="similar-overlay">
          <el-icon><ZoomIn /></el-icon>
        </div>
        <div class="similar-badge">{{ index + 1 }}</div>
      </div>
    </template>

    <!-- 空状态 -->
    <div v-else class="empty-state">
      <el-icon :size="64" class="empty-icon">
        <Collection />
      </el-icon>
      <p class="empty-title">暂无相似商品</p>
      <p class="empty-description">{{ emptyText }}</p>
    </div>

    <!-- 图片预览对话框 -->
    <el-image-viewer
      v-if="showViewer"
      :url-list="previewList"
      :initial-index="previewIndex"
      @close="showViewer = false"
    />
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from "vue";
import {
  Loading,
  PictureFilled,
  ZoomIn,
  Collection,
} from "@element-plus/icons-vue";

interface Props {
  /** 图片列表（索引或URL） */
  images: (number | string)[];
  /** 图片基础路径 */
  basePath?: string;
  /** 空状态文本 */
  emptyText?: string;
}

const props = withDefaults(defineProps<Props>(), {
  basePath: "/dataset",
  emptyText: "点击「相似商品」按钮获取推荐...",
});

// 预览状态
const showViewer = ref(false);
const previewIndex = ref(0);

// 获取图片URL
const getImageUrl = (image: number | string): string => {
  if (typeof image === "string") {
    return image.startsWith("http") || image.startsWith("/")
      ? image
      : `${props.basePath}/${image}`;
  }
  return `${props.basePath}/${image}.jpg`;
};

// 预览列表
const previewList = computed(() => props.images.map((img) => getImageUrl(img)));

// 处理预览
const handlePreview = (index: number) => {
  previewIndex.value = index;
  showViewer.value = true;
};
</script>

<style lang="scss" scoped>
.similar-image-grid {
  display: grid;
  grid-template-columns: repeat(6, 1fr);
  gap: var(--spacing-md, 16px);
  min-height: 150px;

  @media (max-width: 1200px) {
    grid-template-columns: repeat(5, 1fr);
  }

  @media (max-width: 992px) {
    grid-template-columns: repeat(4, 1fr);
  }

  @media (max-width: 768px) {
    grid-template-columns: repeat(3, 1fr);
  }

  @media (max-width: 480px) {
    grid-template-columns: 1fr;
  }
}

.similar-item {
  position: relative;
  border-radius: var(--radius-md, 10px);
  overflow: hidden;
  cursor: pointer;
  background: var(--color-bg-card, #ffffff);
  border: 1px solid var(--color-border, #e2e8f0);
  transition: all 0.3s cubic-bezier(0.34, 1.56, 0.64, 1);

  &:hover {
    transform: scale(1.05);
    box-shadow: var(--shadow-lg, 0 10px 15px -3px rgba(0, 0, 0, 0.1));
    z-index: 10;

    .similar-overlay {
      opacity: 1;
    }

    .similar-image :deep(.el-image__inner) {
      transform: scale(1.1);
    }
  }
}

.similar-image {
  width: 100%;
  height: 100%;

  :deep(.el-image__inner) {
    transition: transform 0.3s ease;
  }
}

.similar-overlay {
  position: absolute;
  inset: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(0, 0, 0, 0.4);
  color: white;
  font-size: 24px;
  opacity: 0;
  transition: opacity 0.3s ease;
}

.similar-badge {
  position: absolute;
  top: 8px;
  left: 8px;
  width: 24px;
  height: 24px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: var(--color-primary, #4f46e5);
  color: white;
  font-size: 12px;
  font-weight: 600;
  border-radius: 50%;
}

.image-loading,
.image-error {
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  background: var(--color-bg-hover, #f1f5f9);
  color: var(--color-text-muted, #9ca3af);
  font-size: 24px;
}

.image-loading .is-loading {
  animation: rotate 1.5s linear infinite;
}

@keyframes rotate {
  from {
    transform: rotate(0deg);
  }
  to {
    transform: rotate(360deg);
  }
}

.empty-state {
  grid-column: 1 / -1;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: var(--spacing-2xl, 48px);
  color: var(--color-text-muted, #9ca3af);
  text-align: center;
}

.empty-icon {
  opacity: 0.5;
  margin-bottom: var(--spacing-md, 16px);
}

.empty-title {
  font-size: var(--font-size-lg, 18px);
  font-weight: 500;
  margin-bottom: var(--spacing-sm, 8px);
}

.empty-description {
  font-size: var(--font-size-sm, 14px);
}
</style>
