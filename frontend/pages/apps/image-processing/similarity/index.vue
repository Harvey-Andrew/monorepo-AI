<template>
  <div class="app-page">
    <header class="page-header">
      <NuxtLink to="/" class="back-link">
        <el-icon><ArrowLeft /></el-icon>
        返回首页
      </NuxtLink>
      <h1 class="page-title">相似检索</h1>
      <p class="page-desc">查找相似商品图片</p>
    </header>

    <main class="main-content">
      <div class="upload-section">
        <BaseUploader @select="handleFileSelect" @clear="handleClear" />
        <div v-if="selectedFile" class="search-options">
          <span>返回数量：</span>
          <el-input-number
            v-model="numImages"
            :min="1"
            :max="50"
            size="small"
          />
        </div>
      </div>

      <div v-if="imagePreview" class="result-section">
        <div class="action-bar">
          <el-button
            type="primary"
            size="large"
            :loading="loading"
            :disabled="!selectedFile"
            @click="handleSearch"
          >
            {{ loading ? "搜索中..." : "开始搜索" }}
          </el-button>
        </div>

        <div v-if="results.length" class="similar-grid">
          <div
            v-for="(url, index) in results"
            :key="index"
            class="similar-item"
            @click="handlePreview(index)"
          >
            <el-image :src="url" fit="cover" lazy class="similar-image">
              <template #error>
                <div class="image-error">
                  <el-icon><Picture /></el-icon>
                </div>
              </template>
            </el-image>
            <div class="similar-badge">{{ index + 1 }}</div>
          </div>
        </div>
      </div>
    </main>

    <el-image-viewer
      v-if="showViewer"
      :url-list="results"
      :initial-index="viewerIndex"
      @close="showViewer = false"
    />
  </div>
</template>

<script setup lang="ts">
import { ref } from "vue";
import { ArrowLeft, Picture } from "@element-plus/icons-vue";
import { ElMessage } from "element-plus";
import { request } from "~/utils/request";

const selectedFile = ref<File | null>(null);
const imagePreview = ref("");
const numImages = ref(10);
const results = ref<string[]>([]);
const loading = ref(false);
const showViewer = ref(false);
const viewerIndex = ref(0);

const handleFileSelect = (file: File) => {
  selectedFile.value = file;
  const reader = new FileReader();
  reader.onload = (e) => {
    imagePreview.value = e.target?.result as string;
    results.value = [];
  };
  reader.readAsDataURL(file);
};

const handleClear = () => {
  selectedFile.value = null;
  imagePreview.value = "";
  results.value = [];
};

const handleSearch = async () => {
  if (!selectedFile.value) return;

  loading.value = true;
  try {
    const formData = new FormData();
    formData.append("image", selectedFile.value);
    formData.append("num_images", numImages.value.toString());

    const res = await request.upload<{ image_urls: string[] }>(
      "/simimages",
      formData
    );
    results.value = res.image_urls;
  } finally {
    loading.value = false;
  }
};

const handlePreview = (index: number) => {
  viewerIndex.value = index;
  showViewer.value = true;
};

useSeoMeta({
  title: "相似检索 - My Local AI Hub",
});
</script>

<style lang="scss" scoped>
.app-page {
  max-width: 1200px;
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
  margin-bottom: 24px;
}

.search-options {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-top: 16px;
  font-size: 14px;
  color: var(--el-text-color-secondary);
}

.action-bar {
  display: flex;
  justify-content: center;
  margin-bottom: 24px;
}

.similar-grid {
  display: grid;
  grid-template-columns: repeat(5, 1fr);
  gap: 12px;

  @media (max-width: 1024px) {
    grid-template-columns: repeat(4, 1fr);
  }

  @media (max-width: 768px) {
    grid-template-columns: repeat(3, 1fr);
  }

  @media (max-width: 480px) {
    grid-template-columns: repeat(2, 1fr);
  }
}

.similar-item {
  position: relative;
  aspect-ratio: 1;
  border-radius: 8px;
  overflow: hidden;
  cursor: pointer;
  border: 1px solid var(--el-border-color);
  transition: all 0.3s ease;

  &:hover {
    transform: scale(1.05);
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
    z-index: 10;
  }
}

.similar-image {
  width: 100%;
  height: 100%;
}

.similar-badge {
  position: absolute;
  top: 6px;
  left: 6px;
  width: 20px;
  height: 20px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: var(--el-color-primary);
  color: white;
  font-size: 10px;
  font-weight: 600;
  border-radius: 50%;
}

.image-error {
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  background: var(--el-fill-color-lighter);
  color: var(--el-text-color-placeholder);
}
</style>
