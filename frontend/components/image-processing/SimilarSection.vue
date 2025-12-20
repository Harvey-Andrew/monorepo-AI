<template>
  <el-card class="content-section similar-section">
    <template #header>
      <div class="section-header">
        <div class="header-left">
          <el-button
            type="warning"
            :icon="loading ? Loading : Search"
            :disabled="disabled || loading"
            @click="$emit('find-similar')"
          >
            {{ loading ? "搜索中..." : "相似商品推荐" }}
          </el-button>
          <el-tag v-if="images.length" type="primary" size="small">
            {{ images.length }} 件
          </el-tag>
          <el-input-number
            :model-value="similarCount"
            size="small"
            :min="1"
            :max="50"
            style="width: 100px; margin-left: 8px"
            @update:model-value="$emit('update:similar-count', $event)"
          />件
        </div>
      </div>
    </template>

    <ImageProcessingSimilarImageGrid
      :images="images"
      :loading="loading"
      :empty-text="emptyText"
    />
  </el-card>
</template>

<script setup lang="ts">
import { Search, Loading } from "@element-plus/icons-vue";

// Props
withDefaults(
  defineProps<{
    images: string[];
    loading: boolean;
    similarCount: number;
    disabled?: boolean;
    emptyText?: string;
  }>(),
  {
    disabled: false,
    emptyText: "完成去噪后，点击「相似商品推荐」获取推荐",
  }
);

// Events
defineEmits<{
  (e: "find-similar"): void;
  (e: "update:similar-count", value: number): void;
}>();
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
</style>
