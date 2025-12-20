<template>
  <div class="image-canvas" :style="canvasStyle">
    <el-image
      v-if="src"
      :src="src"
      :fit="fit"
      :preview-src-list="preview ? [src] : undefined"
      :preview-teleported="true"
      class="canvas-image"
    >
      <template #placeholder>
        <div class="image-loading">
          <el-icon class="is-loading"><Loading /></el-icon>
        </div>
      </template>
      <template #error>
        <div class="image-error">
          <el-icon><PictureFilled /></el-icon>
          <span>加载失败</span>
        </div>
      </template>
    </el-image>
    <div v-else class="image-placeholder">
      <el-icon :size="48" class="placeholder-icon">
        <slot name="icon">
          <Picture />
        </slot>
      </el-icon>
      <span class="placeholder-text">
        <slot name="placeholder">{{ placeholder }}</slot>
      </span>
    </div>
    <slot></slot>
  </div>
</template>

<script setup lang="ts">
import { computed } from "vue";
import { Loading, PictureFilled, Picture } from "@element-plus/icons-vue";

interface Props {
  src?: string;
  width?: string | number;
  height?: string | number;
  fit?: "contain" | "cover" | "fill" | "none" | "scale-down";
  placeholder?: string;
  preview?: boolean;
}

const props = withDefaults(defineProps<Props>(), {
  src: "",
  width: "100%",
  height: "200px",
  fit: "contain",
  placeholder: "暂无图片",
  preview: true,
});

const canvasStyle = computed(() => ({
  width: typeof props.width === "number" ? `${props.width}px` : props.width,
  height: typeof props.height === "number" ? `${props.height}px` : props.height,
}));
</script>

<style lang="scss" scoped>
.image-canvas {
  position: relative;
  display: flex;
  align-items: center;
  justify-content: center;
  background: var(--el-fill-color-lighter);
  border-radius: 8px;
  overflow: hidden;
}

.canvas-image {
  width: 100%;
  height: 100%;
}

.image-placeholder {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 8px;
}

.placeholder-icon {
  color: var(--el-text-color-placeholder);
  opacity: 0.5;
}

.placeholder-text {
  color: var(--el-text-color-placeholder);
  font-size: 14px;
}

.image-loading,
.image-error {
  width: 100%;
  height: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 8px;
  background: var(--el-fill-color-lighter);
  color: var(--el-text-color-placeholder);
}

.is-loading {
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
</style>
