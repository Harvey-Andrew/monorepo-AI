<template>
  <Teleport to="body">
    <Transition name="fade">
      <div v-if="loading" class="global-loading">
        <div class="loading-content">
          <div class="loading-logo">🤖</div>
          <div class="loading-spinner"></div>
          <p class="loading-text">正在加载...</p>
        </div>
      </div>
    </Transition>
  </Teleport>
</template>

<script setup lang="ts">
defineProps<{
  loading: boolean;
}>();
</script>

<style scoped lang="scss"></style>
