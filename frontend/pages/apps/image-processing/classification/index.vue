<template>
  <div class="app-page">
    <header class="page-header">
      <NuxtLink to="/" class="back-link">
        <el-icon><ArrowLeft /></el-icon>
        返回首页
      </NuxtLink>
      <h1 class="page-title">商品分类</h1>
      <p class="page-desc">识别商品类别（上衣、鞋、包、下身衣服、手表）</p>
    </header>

    <main class="main-content">
      <div class="upload-section">
        <BaseUploader @select="handleFileSelect" @clear="handleClear" />
      </div>

      <div v-if="imagePreview" class="result-section">
        <div class="result-grid">
          <div class="result-item">
            <h3 class="result-title">上传图片</h3>
            <ImageCanvas :src="imagePreview" />
          </div>

          <div class="result-item result-display">
            <h3 class="result-title">分类结果</h3>
            <div class="classification-result">
              <el-tag v-if="result" type="success" size="large">
                {{ result }}
              </el-tag>
              <span v-else class="no-result">点击下方按钮进行分类</span>
            </div>
          </div>
        </div>

        <div class="action-bar">
          <el-button
            type="primary"
            size="large"
            :loading="loading"
            :disabled="!selectedFile"
            @click="handleClassify"
          >
            {{ loading ? "识别中..." : "开始分类" }}
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

const selectedFile = ref<File | null>(null);
const imagePreview = ref("");
const result = ref("");
const loading = ref(false);

const handleFileSelect = (file: File) => {
  selectedFile.value = file;
  const reader = new FileReader();
  reader.onload = (e) => {
    imagePreview.value = e.target?.result as string;
    result.value = "";
  };
  reader.readAsDataURL(file);
};

const handleClear = () => {
  selectedFile.value = null;
  imagePreview.value = "";
  result.value = "";
};

const handleClassify = async () => {
  if (!selectedFile.value) return;

  loading.value = true;
  try {
    const formData = new FormData();
    formData.append("image", selectedFile.value);

    const res = await request.upload<{ result: string }>(
      "/classification",
      formData
    );
    result.value = res.result;
    ElMessage.success("分类完成");
  } catch (e: any) {
    ElMessage.error(e.message || "分类失败");
  } finally {
    loading.value = false;
  }
};

useSeoMeta({
  title: "商品分类 - My Local AI Hub",
});
</script>

<style lang="scss" scoped>
.app-page {
  max-width: 800px;
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
  grid-template-columns: 1fr 1fr;
  gap: 16px;
  margin-bottom: 24px;

  @media (max-width: 640px) {
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
}

.result-display {
  display: flex;
  flex-direction: column;
}

.classification-result {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 150px;
}

.no-result {
  color: var(--el-text-color-placeholder);
  font-size: 14px;
}

.action-bar {
  display: flex;
  justify-content: center;
}
</style>
