<template>
  <div class="base-uploader">
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
        <span class="upload-text">{{ placeholder }}</span>
      </template>
      <template v-else>
        <div class="preview-container">
          <el-image :src="previewUrl" fit="contain" class="preview-image" />
          <div class="reselect-btn">
            <el-icon :size="12"><Refresh /></el-icon>
            <span>重新选择</span>
          </div>
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
  maxSize?: number;
  placeholder?: string;
}

const props = withDefaults(defineProps<Props>(), {
  maxSize: 10,
  placeholder: "上传图片",
});

const emit = defineEmits<{
  (e: "select", file: File): void;
  (e: "clear"): void;
}>();

const uploadRef = ref<UploadInstance>();
const selectedFile = ref<File | null>(null);

const previewUrl = computed(() => {
  if (!selectedFile.value) return "";
  return URL.createObjectURL(selectedFile.value);
});

const handleChange = (uploadFile: UploadFile) => {
  const file = uploadFile.raw as File;
  if (!file.type.startsWith("image/")) {
    ElMessage.warning("请选择图片文件");
    return;
  }
  if (file.size > props.maxSize * 1024 * 1024) {
    ElMessage.warning(`图片大小不能超过 ${props.maxSize}MB`);
    return;
  }
  selectedFile.value = file;
  emit("select", file);
};

const handleExceed = (files: File[]) => {
  if (files.length > 0) {
    uploadRef.value?.clearFiles();
    const file = files[0] as UploadRawFile;
    handleChange({ raw: file } as UploadFile);
  }
};

const clearFile = () => {
  selectedFile.value = null;
  uploadRef.value?.clearFiles();
  emit("clear");
};

defineExpose({ clearFile });
</script>

<style lang="scss" scoped>
.base-uploader {
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
    padding: 8px;
    border-radius: 8px;
    border: 2px dashed var(--el-border-color);
    background: var(--el-fill-color-lighter);
    transition: all 0.25s ease;

    &:hover,
    &.is-dragover {
      border-color: var(--el-color-primary);
      background: var(--el-color-primary-light-9);
    }
  }
}

.upload-icon {
  color: var(--el-color-primary);
  margin-bottom: 4px;
}

.upload-text {
  font-size: 14px;
  color: var(--el-text-color-secondary);
}

.preview-container {
  position: relative;
  width: 100%;
  height: 100%;
  overflow: hidden;
  border-radius: 6px;
}

.preview-image {
  width: 100%;
  height: 100%;
}

.delete-btn,
.reselect-btn {
  position: absolute;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.2s ease;
  z-index: 10;
}

.delete-btn {
  top: 4px;
  right: 4px;
  width: 20px;
  height: 20px;
  background: rgba(0, 0, 0, 0.6);
  color: white;
  border-radius: 50%;

  &:hover {
    background: var(--el-color-danger);
    transform: scale(1.1);
  }
}

.reselect-btn {
  top: 4px;
  left: 4px;
  gap: 2px;
  padding: 4px 8px;
  background: rgba(0, 0, 0, 0.6);
  color: white;
  font-size: 10px;
  border-radius: 4px;

  &:hover {
    background: var(--el-color-primary);
  }
}
</style>
