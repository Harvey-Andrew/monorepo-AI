<template>
  <el-card class="content-section">
    <template #header>
      <div class="section-header">
        <div class="header-left">
          <el-icon class="section-icon" :size="24">
            <Picture />
          </el-icon>
          <span class="section-title">处理过程</span>
        </div>
        <el-button
          v-if="originalImage"
          type="primary"
          :icon="isLoading ? Loading : VideoPlay"
          :disabled="isLoading"
          @click="$emit('process-all')"
        >
          {{ isLoading ? "处理中..." : "一步到位" }}
        </el-button>
        <el-button
          v-if="originalImage"
          type="danger"
          link
          :icon="Delete"
          @click="$emit('clear-image')"
        >
          清空所有
        </el-button>
      </div>
    </template>

    <div class="preview-grid">
      <!-- 上传/原始图片（合并） -->
      <el-card class="preview-card" shadow="hover">
        <template #header>
          <div class="card-header">
            <div class="card-header-left">
              <el-icon class="card-icon" :size="20">
                <Upload />
              </el-icon>
              <span class="card-title">原始图片</span>
            </div>
          </div>
        </template>
        <div class="card-body">
          <template v-if="originalImage">
            <div class="image-with-actions">
              <el-image
                :src="originalImage"
                fit="contain"
                class="preview-image"
                :preview-src-list="[originalImage]"
                :preview-teleported="true"
              />
              <!-- 隐藏的文件选择输入框 -->
              <input
                ref="fileInputRef"
                type="file"
                accept="image/*"
                class="hidden-file-input"
                @change="handleFileInputChange"
              />
              <!-- 悬浮操作按钮 -->
              <div class="hover-actions">
                <!-- 左上角重新选择按钮 -->
                <div class="reselect-btn" @click.stop="triggerReselect">
                  <el-icon :size="12"><Refresh /></el-icon>
                  <span>重新选择</span>
                </div>
                <!-- 右上角删除按钮 -->
                <div class="delete-btn" @click.stop="$emit('clear-image')">
                  <el-icon :size="12"><Close /></el-icon>
                </div>
              </div>
            </div>
          </template>
          <template v-else>
            <ImageProcessingImageUploader
              ref="uploaderRef"
              @select="$emit('file-select', $event)"
              @clear="$emit('file-clear')"
            />
          </template>
        </div>
      </el-card>

      <!-- 噪声图片 -->
      <el-card class="preview-card" shadow="hover">
        <template #header>
          <div class="card-header">
            <div class="card-header-left">
              <el-icon class="card-icon" :size="20">
                <MagicStick />
              </el-icon>
              <span class="card-title">噪声图片</span>
            </div>
          </div>
        </template>
        <div class="card-body">
          <template v-if="isLoading && currentAction === 'denoise'">
            <el-icon class="is-loading" :size="32">
              <Loading />
            </el-icon>
            <span class="loading-text">处理中...</span>
          </template>
          <template v-else-if="noisyImage">
            <el-image
              :src="noisyImage"
              fit="contain"
              class="preview-image"
              :preview-src-list="[noisyImage]"
              :preview-teleported="true"
            />
          </template>
          <template v-else>
            <el-icon :size="48" class="empty-icon">
              <MagicStick />
            </el-icon>
            <span class="empty-text">去噪处理后显示</span>
          </template>
        </div>
      </el-card>

      <!-- 去噪结果（带按钮） -->
      <el-card class="preview-card" shadow="hover">
        <template #header>
          <div class="card-header">
            <div class="card-header-left">
              <el-button
                type="primary"
                size="small"
                :icon="
                  isLoading && currentAction === 'denoise' ? Loading : Brush
                "
                :disabled="!originalImage || isLoading"
                @click="$emit('denoise')"
              >
                {{
                  isLoading && currentAction === "denoise"
                    ? "处理中..."
                    : "图像去噪"
                }}
              </el-button>
            </div>
          </div>
        </template>
        <div class="card-body">
          <template v-if="isLoading && currentAction === 'denoise'">
            <el-icon class="is-loading" :size="32">
              <Loading />
            </el-icon>
            <span class="loading-text">处理中...</span>
          </template>
          <template v-else-if="denoisedImage">
            <el-image
              :src="denoisedImage"
              fit="contain"
              class="preview-image"
              :preview-src-list="[denoisedImage]"
              :preview-teleported="true"
            />
          </template>
          <template v-else>
            <el-icon :size="48" class="empty-icon">
              <Finished />
            </el-icon>
            <span class="empty-text">去噪处理后显示</span>
          </template>
        </div>
      </el-card>

      <!-- 商品类型（带按钮） -->
      <el-card class="preview-card type-card" shadow="hover">
        <template #header>
          <div class="card-header">
            <div class="card-header-left">
              <el-button
                type="success"
                size="small"
                :icon="
                  isLoading && currentAction === 'classify'
                    ? Loading
                    : Histogram
                "
                :disabled="!denoisedImage || isLoading"
                @click="$emit('classify')"
              >
                {{
                  isLoading && currentAction === "classify"
                    ? "识别中..."
                    : "商品分类"
                }}
              </el-button>
            </div>
          </div>
        </template>
        <div class="card-body">
          <template v-if="isLoading && currentAction === 'classify'">
            <el-icon class="is-loading" :size="32">
              <Loading />
            </el-icon>
            <span class="loading-text">识别中...</span>
          </template>
          <template v-else-if="classificationResult">
            <el-tag type="warning" size="large" class="classification-tag">
              {{ classificationResult }}
            </el-tag>
          </template>
          <template v-else>
            <el-icon :size="48" class="empty-icon">
              <PriceTag />
            </el-icon>
            <span class="empty-text">待分类</span>
          </template>
        </div>
      </el-card>
    </div>
  </el-card>
</template>

<script setup lang="ts">
import { ref } from "vue";
import {
  Upload,
  Picture,
  Brush,
  Histogram,
  Loading,
  MagicStick,
  Refresh,
  Close,
  PriceTag,
  Delete,
  VideoPlay,
  Finished,
} from "@element-plus/icons-vue";

// Props
defineProps<{
  originalImage: string;
  noisyImage: string;
  denoisedImage: string;
  classificationResult: string;
  isLoading: boolean;
  currentAction: string;
}>();

// Events
const emit = defineEmits<{
  (e: "file-select", file: File): void;
  (e: "file-clear"): void;
  (e: "clear-image"): void;
  (e: "denoise"): void;
  (e: "classify"): void;
  (e: "process-all"): void;
}>();

// 上传组件引用
const uploaderRef = ref();

// 文件输入框引用
const fileInputRef = ref<HTMLInputElement>();

// 触发重新选择图片
const triggerReselect = () => {
  fileInputRef.value?.click();
};

// 处理文件输入变更
const handleFileInputChange = (event: Event) => {
  const input = event.target as HTMLInputElement;
  if (input.files && input.files[0]) {
    emit("file-select", input.files[0]);
    // 重置 input 以便可以选择同一文件
    input.value = "";
  }
};
</script>

<style lang="scss" scoped>
.content-section {
  --el-card-border-radius: var(--radius-lg, 16px);
}

.section-header {
  display: flex;
  align-items: center;
  gap: var(--spacing-md, 16px);
  flex-wrap: wrap;
}

.header-left {
  display: flex;
  align-items: center;
  gap: var(--spacing-sm, 8px);
}

.section-icon {
  color: var(--color-primary, #4f46e5);
}

.section-title {
  font-size: var(--font-size-lg, 18px);
  font-weight: 600;
}

.preview-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: var(--spacing-lg, 24px);

  @media (max-width: 1200px) {
    grid-template-columns: repeat(2, 1fr);
  }

  @media (max-width: 768px) {
    grid-template-columns: 1fr;
  }
}

.preview-card {
  height: 100%;
  transition: all var(--transition-normal, 0.25s ease);

  &:hover {
    transform: translateY(-4px);
  }
}

.card-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: var(--spacing-sm, 8px);

  &-left {
    display: flex;
    align-items: center;
    gap: var(--spacing-sm, 8px);
  }
}

.card-icon {
  color: var(--color-primary, #4f46e5);
}

.card-title {
  font-weight: 600;
  font-size: var(--font-size-md, 16px);
}

.card-body {
  min-height: 200px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  background: var(--color-bg-page, #f8fafc);
  border-radius: var(--radius-md, 10px);
  overflow: hidden;

  .preview-image {
    width: 100%;
    height: 200px;
    cursor: zoom-in;
  }

  .empty-icon {
    color: var(--color-text-muted, #9ca3af);
    opacity: 0.5;
    margin-bottom: var(--spacing-sm, 8px);
  }

  .empty-text {
    color: var(--color-text-muted, #9ca3af);
    font-size: var(--font-size-sm, 14px);
  }
}

.image-with-actions {
  position: relative;
  width: 100%;
  height: 100%;

  .preview-image {
    width: 100%;
    height: 200px;
  }

  &:hover .hover-actions {
    opacity: 1;
  }
}

.hidden-file-input {
  display: none !important;
}

.hover-actions {
  position: absolute;
  inset: 0;
  opacity: 0;
  transition: opacity 0.2s ease;
  pointer-events: none;

  .reselect-btn,
  .delete-btn {
    pointer-events: auto;
  }

  .reselect-btn {
    position: absolute;
    top: 8px;
    left: 8px;
    display: flex;
    align-items: center;
    gap: 4px;
    padding: 6px 10px;
    background: transparent;
    color: black;
    font-size: 12px;
    border-radius: 6px;
    cursor: pointer;
    transition: all 0.2s ease;
    z-index: 10;

    &:hover {
      color: var(--color-primary, #4f46e5);
    }
  }

  .delete-btn {
    position: absolute;
    top: 8px;
    right: 8px;
    width: 28px;
    height: 28px;
    display: flex;
    align-items: center;
    justify-content: center;
    background: transparent;
    color: black;
    border-radius: 50%;
    cursor: pointer;
    transition: all 0.2s ease;
    z-index: 10;

    &:hover {
      color: var(--color-danger, #ef4444);
      transform: scale(1.1);
    }
  }
}

.is-loading {
  animation: rotate 1s linear infinite;
  color: var(--color-primary, #4f46e5);
}

@keyframes rotate {
  from {
    transform: rotate(0deg);
  }
  to {
    transform: rotate(360deg);
  }
}

.loading-text {
  font-size: var(--font-size-sm, 14px);
  color: var(--color-text-muted, #9ca3af);
  margin-top: var(--spacing-sm, 8px);
}

.type-card {
  height: 100%;
  transition: all var(--transition-normal, 0.25s ease);

  &:hover {
    transform: translateY(-4px);
  }
}

// 分类结果标签放大样式
.classification-tag {
  font-size: 32px !important;
  padding: 16px 32px !important;
  height: auto !important;
  line-height: 1.5 !important;
}
</style>
