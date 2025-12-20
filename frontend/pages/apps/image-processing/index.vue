<template>
  <div class="page-container">
    <!-- 返回链接 -->
    <header class="page-nav">
      <NuxtLink to="/" class="back-link">
        <el-icon><ArrowLeft /></el-icon>
        返回首页
      </NuxtLink>
    </header>

    <!-- 页面头部 -->
    <ImageProcessingPageHeader />

    <!-- 主内容区 -->
    <main class="main-content">
      <!-- 处理结果区块 -->
      <ImageProcessingProcessSection
        :original-image="originalImage"
        :noisy-image="noisyImage"
        :denoised-image="denoisedImage"
        :classification-result="classificationResult"
        :is-loading="isLoading"
        :current-action="currentAction"
        @file-select="handleFileSelect"
        @file-clear="handleFileClear"
        @clear-image="handleClearImage"
        @denoise="handleDenoise"
        @classify="handleClassify"
        @process-all="handleProcessAll"
      />

      <!-- 相似商品区块 -->
      <ImageProcessingSimilarSection
        :images="similarImages"
        :loading="isLoading && currentAction === 'similar'"
        :similar-count="similarCount"
        :disabled="!denoisedImage"
        @find-similar="handleFindSimilar"
        @update:similar-count="similarCount = $event"
      />
    </main>
  </div>
</template>

<script setup lang="ts">
import { ref, watch } from "vue";
import { ArrowLeft } from "@element-plus/icons-vue";
import { ElMessage } from "element-plus";
import { useDebounceFn } from "@vueuse/core";
import { DEBOUNCE_DELAY } from "~/constants/time";
import { useImageProcess } from "~/composables/useImageProcess";

// 使用图像处理 Composable
const {
  originalImage,
  noisyImage,
  denoisedImage,
  classificationResult,
  similarImages,
  isLoading,
  error,
  uploadImage,
  denoise,
  classify,
  findSimilar,
  clearError,
} = useImageProcess();

// 选中的文件
const selectedFile = ref<File | null>(null);

// 当前操作
const currentAction = ref<string>("");

// 相似推荐数量
const similarCount = ref<number>(10);

// 处理文件选择（选择后自动上传）
const handleFileSelect = async (file: File) => {
  selectedFile.value = file;
  try {
    await uploadImage(file);
  } catch {
    console.log("上传失败");
  }
};

// 处理文件清除
const handleFileClear = () => {
  selectedFile.value = null;
};

// 清除已上传的图片
const handleClearImage = () => {
  originalImage.value = "";
  noisyImage.value = "";
  denoisedImage.value = "";
  classificationResult.value = "";
  similarImages.value = [];
  selectedFile.value = null;
};

// 图像去噪
const handleDenoise = async () => {
  if (!originalImage.value) {
    ElMessage.warning("请先上传图片");
    return;
  }
  currentAction.value = "denoise";
  try {
    await denoise();
  } finally {
    currentAction.value = "";
  }
};

// 商品分类
const handleClassify = async () => {
  if (!denoisedImage.value) {
    ElMessage.warning("请先进行去噪处理");
    return;
  }
  currentAction.value = "classify";
  try {
    await classify();
  } finally {
    currentAction.value = "";
  }
};

// 相似商品
const handleFindSimilar = async () => {
  if (!denoisedImage.value) {
    ElMessage.warning("请先进行去噪处理");
    return;
  }
  currentAction.value = "similar";
  try {
    await findSimilar(similarCount.value);
  } finally {
    currentAction.value = "";
  }
};

// 一步到位：依次执行去噪、分类、相似推荐
const handleProcessAll = useDebounceFn(async () => {
  if (!originalImage.value) {
    ElMessage.warning("请先上传图片");
    return;
  }

  try {
    // 步骤1：去噪
    currentAction.value = "denoise";
    await denoise();

    // 步骤2：分类
    currentAction.value = "classify";
    await classify();

    // 步骤3：相似推荐
    currentAction.value = "similar";
    await findSimilar(similarCount.value);
  } finally {
    currentAction.value = "";
  }
}, DEBOUNCE_DELAY);

// 监听错误
watch(error, (newError) => {
  if (newError) {
    ElMessage.error(newError);
    clearError();
  }
});

// SEO 元信息
useSeoMeta({
  title: "智图寻宝 - 智能商品识别系统",
  description:
    "基于深度学习的智能商品识别系统，支持图像去噪、商品分类、相似商品推荐",
  ogTitle: "智图寻宝 - 智能商品识别系统",
  ogDescription: "基于深度学习的智能商品识别系统",
  ogType: "website",
});
</script>

<style lang="scss" scoped>
.page-nav {
  margin-bottom: var(--spacing-md, 16px);
}

.back-link {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  font-size: 14px;
  color: var(--color-text-secondary, #6b7280);
  text-decoration: none;
  transition: var(--transition-normal, 250ms ease);

  &:hover {
    color: var(--color-primary, #4f46e5);
  }
}
</style>
