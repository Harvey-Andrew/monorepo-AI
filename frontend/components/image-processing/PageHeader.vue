<template>
  <header class="page-header">
    <div class="brand-section">
      <img
        src="/image-processing/智图寻宝.png"
        alt="智图寻宝"
        class="brand-logo"
      />
      <div class="brand-divider"></div>
      <div class="brand-info">
        <h1 class="brand-title">智能商品识别系统</h1>
        <p class="brand-subtitle">图像去噪 · 商品分类 · 相似推荐</p>
      </div>
    </div>
  </header>
</template>

<script setup lang="ts">
// 页面头部组件 - 展示品牌 Logo、标题和副标题
</script>

<style lang="scss" scoped>
.page-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: var(--spacing-xl, 32px);
  padding-bottom: var(--spacing-lg, 24px);
  border-bottom: 1px solid var(--color-border, #e2e8f0);

  @media (max-width: 576px) {
    flex-direction: column;
    align-items: flex-start;
    gap: var(--spacing-md, 16px);
  }
}

.brand-section {
  display: flex;
  align-items: center;
  gap: var(--spacing-md, 16px);
}

.brand-logo {
  height: 48px;
  object-fit: contain;
}

.brand-divider {
  height: 40px;
  width: 2px;
  background: linear-gradient(
    180deg,
    transparent,
    var(--color-primary, #4f46e5),
    transparent
  );
  border-radius: var(--radius-full, 9999px);
}

.brand-info {
  display: flex;
  flex-direction: column;
}

.brand-title {
  font-size: var(--font-size-xl, 20px);
  font-weight: 600;
  color: var(--color-text-primary, #1f2937);
  margin: 0;
}

.brand-subtitle {
  font-size: var(--font-size-sm, 14px);
  color: var(--color-text-secondary, #6b7280);
  margin: var(--spacing-xs, 4px) 0 0;
}
</style>
