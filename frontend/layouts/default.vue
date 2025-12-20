<template>
  <div class="default-layout">
    <!-- 全局加载遮罩 -->
    <GlobalLoading :loading="isLoading" />

    <!-- 页面内容 -->
    <slot />
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from "vue";

const isLoading = ref(true);

onMounted(() => {
  setTimeout(() => {
    isLoading.value = false;
  }, 1000);
});
</script>

<style scoped></style>
