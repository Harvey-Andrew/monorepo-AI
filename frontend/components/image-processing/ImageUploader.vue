<template>
  <div class="image-uploader">
    <el-upload
      ref="uploadRef"
      class="upload-dragger"
      drag
      :auto-upload="false"
      :show-file-list="false"
      :limit="1"
      accept="image/*"
      :on-change="handleChange"
      :on-exceed="handleExceed"
    >
      <template v-if="!previewUrl">
        <el-icon class="upload-icon" :size="32">
          <UploadFilled />
        </el-icon>
        <span class="upload-text">上传图片</span>
      </template>
      <template v-else>
        <div class="preview-container">
          <el-image :src="previewUrl" fit="contain" class="preview-image" />
          <!-- 左上角重新选择按钮 -->
          <div class="reselect-btn">
            <el-icon :size="12"><Refresh /></el-icon>
            <span>重新选择</span>
          </div>
          <!-- 右上角删除按钮 -->
          <div class="delete-btn" @click.stop="clearFile">
            <el-icon :size="12"><Close /></el-icon>
          </div>
        </div>
      </template>
    </el-upload>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from "vue";
import { ElMessage } from "element-plus";
import { UploadFilled, Close, Refresh } from "@element-plus/icons-vue";
import type { UploadFile, UploadInstance, UploadRawFile } from "element-plus";

interface Props {
  /** 最大文件大小（MB） */
  maxSize?: number;
}

const props = withDefaults(defineProps<Props>(), {
  maxSize: 10,
});

const emit = defineEmits<{
  (e: "select", file: File): void;
  (e: "clear"): void;
}>();

// 上传组件引用
const uploadRef = ref<UploadInstance>();

// 选中的文件
const selectedFile = ref<File | null>(null);

// 预览URL
const previewUrl = computed(() => {
  if (!selectedFile.value) return "";
  return URL.createObjectURL(selectedFile.value);
});

// 处理文件变更
const handleChange = (uploadFile: UploadFile) => {
  const file = uploadFile.raw as File;

  // 验证文件类型
  if (!file.type.startsWith("image/")) {
    ElMessage.warning("请选择图片文件");
    return;
  }

  // 验证文件大小
  if (file.size > props.maxSize * 1024 * 1024) {
    ElMessage.warning(`图片大小不能超过 ${props.maxSize}MB`);
    return;
  }

  selectedFile.value = file;
  emit("select", file);
};

// 处理超出限制
const handleExceed = (files: File[]) => {
  // 替换现有文件
  if (files.length > 0) {
    uploadRef.value?.clearFiles();
    const file = files[0] as UploadRawFile;
    handleChange({ raw: file } as UploadFile);
  }
};

// 清除文件
const clearFile = () => {
  selectedFile.value = null;
  uploadRef.value?.clearFiles();
  emit("clear");
};

// 格式化文件大小
const formatFileSize = (bytes: number): string => {
  if (bytes < 1024) return bytes + " B";
  if (bytes < 1024 * 1024) return (bytes / 1024).toFixed(1) + " KB";
  return (bytes / (1024 * 1024)).toFixed(1) + " MB";
};

// 暴露方法
defineExpose({
  clearFile,
});
</script>

<style lang="scss" scoped>
.image-uploader {
  width: 100%;
  height: 200px;
}

.upload-dragger {
  width: 100%;
  height: 100%;

  :deep(.el-upload) {
    width: 100%;
    height: 100%;
  }

  :deep(.el-upload-dragger) {
    width: 100%;
    height: 100%;
    min-height: 0;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: var(--spacing-xs, 4px);
    border-radius: var(--radius-sm, 6px);
    border: 2px dashed var(--color-border, #e2e8f0);
    background: var(--color-bg-page, #f8fafc);
    transition: all 0.25s ease;

    &:hover,
    &.is-dragover {
      border-color: var(--color-primary, #4f46e5);
      background: var(--color-primary-bg, rgba(79, 70, 229, 0.1));
    }
  }
}

.upload-icon {
  color: var(--color-primary, #4f46e5);
  margin-bottom: 4px;
}

.upload-text {
  font-size: 14px;
  color: var(--color-text-secondary, #6b7280);

  em {
    color: var(--color-primary, #4f46e5);
    font-style: normal;
    font-weight: 500;
  }
}

.upload-hint {
  font-size: var(--font-size-sm, 14px);
  color: var(--color-text-muted, #9ca3af);
  margin-top: var(--spacing-sm, 8px);
}

.preview-container {
  position: relative;
  width: 100%;
  height: 100%;
  overflow: hidden;
  border-radius: var(--radius-sm, 6px);
}

.preview-image {
  width: 100%;
  height: 100%;

  :deep(.el-image__inner) {
    object-fit: contain;
  }
}

.delete-btn {
  position: absolute;
  top: 2px;
  right: 2px;
  width: 16px;
  height: 16px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(0, 0, 0, 0.6);
  color: white;
  border-radius: 50%;
  cursor: pointer;
  transition: all 0.2s ease;
  z-index: 10;

  &:hover {
    background: var(--color-danger, #ef4444);
    transform: scale(1.1);
  }
}

.reselect-btn {
  position: absolute;
  top: 4px;
  left: 4px;
  display: flex;
  align-items: center;
  gap: 2px;
  padding: 2px 6px;
  background: rgba(0, 0, 0, 0.6);
  color: white;
  font-size: 10px;
  border-radius: 4px;
  cursor: pointer;
  transition: all 0.2s ease;
  z-index: 10;

  &:hover {
    background: var(--color-primary, #4f46e5);
  }
}

.file-info {
  display: flex;
  align-items: center;
  gap: var(--spacing-sm, 8px);
  padding: var(--spacing-sm, 8px) var(--spacing-md, 16px);
  margin-top: var(--spacing-md, 16px);
  background: var(--color-bg-hover, #f1f5f9);
  border-radius: var(--radius-md, 10px);
  font-size: var(--font-size-sm, 14px);
}

.file-name {
  flex: 1;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  color: var(--color-text-primary, #1f2937);
}

.file-size {
  color: var(--color-text-muted, #9ca3af);
}

// 过渡动画
.slide-up-enter-active,
.slide-up-leave-active {
  transition: all 0.25s ease;
}

.slide-up-enter-from,
.slide-up-leave-to {
  opacity: 0;
  transform: translateY(10px);
}
</style>
