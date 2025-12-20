<template>
  <div class="app-page">
    <header class="page-header">
      <NuxtLink to="/" class="back-link">
        <el-icon><ArrowLeft /></el-icon>
        返回首页
      </NuxtLink>
      <h1 class="page-title">图像去噪</h1>
      <p class="page-desc">使用卷积自编码器去除图像噪声</p>
    </header>

    <main class="main-content">
      <div class="upload-section">
        <BaseUploader @select="handleFileSelect" @clear="handleClear" />
      </div>

      <div v-if="originalImage" class="result-section">
        <div class="result-grid">
          <div class="result-item">
            <h3 class="result-title">原始图片</h3>
            <ImageCanvas :src="originalImage" />
          </div>

          <div class="result-item">
            <h3 class="result-title">噪声图片</h3>
            <ImageCanvas
              :src="noisyImage ? `data:image/png;base64,${noisyImage}` : ''"
              placeholder="处理后显示"
            />
          </div>

          <div class="result-item">
            <h3 class="result-title">去噪结果</h3>
            <ImageCanvas
              :src="
                denoisedImage ? `data:image/png;base64,${denoisedImage}` : ''
              "
              placeholder="处理后显示"
            />
          </div>
        </div>

        <div class="action-bar">
          <el-button
            type="primary"
            size="large"
            :loading="loading"
            :disabled="!originalImage"
            @click="handleDenoise"
          >
            {{ loading ? "处理中..." : "开始去噪" }}
          </el-button>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup lang="ts">
import { ref } from "vue";
import { ArrowLeft } from "@element-plus/icons-vue";
import { ElMessage } from "element-plus";
import { request } from "~/utils/request";

const originalImage = ref("");
const noisyImage = ref("");
const denoisedImage = ref("");
const loading = ref(false);

const handleFileSelect = (file: File) => {
  const reader = new FileReader();
  reader.onload = (e) => {
    originalImage.value = e.target?.result as string;
    noisyImage.value = "";
    denoisedImage.value = "";
  };
  reader.readAsDataURL(file);
};

const handleClear = () => {
  originalImage.value = "";
  noisyImage.value = "";
  denoisedImage.value = "";
};

const handleDenoise = async () => {
  if (!originalImage.value) return;

  loading.value = true;
  try {
    const response = await fetch(originalImage.value);
    const blob = await response.blob();
    const formData = new FormData();
    formData.append("image", blob, "image.png");

    const result = await request.upload<{
      noisy_img: string;
      denoised_image: string;
    }>("/denoising", formData);

    noisyImage.value = result.noisy_img;
    denoisedImage.value = result.denoised_image;
  } finally {
    loading.value = false;
  }
};

useSeoMeta({
  title: "图像去噪 - My Local AI Hub",
});
</script>

<style lang="scss" scoped>
.app-page {
  max-width: 1000px;
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

  &:hover {
    color: var(--el-color-primary);
  }
}

.page-title {
  font-size: 28px;
  font-weight: 700;
  margin: 0;
}

.page-desc {
  font-size: 14px;
  color: var(--el-text-color-secondary);
  margin: 8px 0 0;
}

.upload-section {
  margin-bottom: 32px;
}

.result-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 16px;
  margin-bottom: 24px;

  @media (max-width: 768px) {
    grid-template-columns: 1fr;
  }
}

.result-item {
  background: var(--el-bg-color);
  border: 1px solid var(--el-border-color);
  border-radius: 12px;
  padding: 16px;
}

.result-title {
  font-size: 14px;
  font-weight: 600;
  margin: 0 0 12px;
  color: var(--el-text-color-primary);
}

.action-bar {
  display: flex;
  justify-content: center;
}
</style>
