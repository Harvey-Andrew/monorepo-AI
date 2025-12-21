<script setup lang="ts">
/**
 * 打字机效果组件
 * 逐字显示内容
 */
const props = withDefaults(
  defineProps<{
    /** 要显示的内容 */
    content: string;
    /** 打字速度（毫秒/字） */
    speed?: number;
    /** 是否正在输入中（流式响应时为true） */
    streaming?: boolean;
  }>(),
  {
    speed: 20,
    streaming: false,
  }
);

const emit = defineEmits<{
  complete: [];
  update: [];
}>();

// 当前显示的文本
const displayText = ref("");
// 当前索引位置
let currentIndex = 0;
// 定时器
let timer: ReturnType<typeof setTimeout> | null = null;

// 打下一个字符
function typeNext() {
  if (currentIndex < props.content.length) {
    displayText.value = props.content.slice(0, currentIndex + 1);
    currentIndex++;
    emit("update");
    timer = setTimeout(typeNext, props.speed);
  } else if (!props.streaming) {
    // 非流式模式下，打字完成
    emit("complete");
  }
}

// 监听内容变化
watch(
  () => props.content,
  (newContent, oldContent) => {
    // 如果是追加内容（流式响应）
    if (newContent.startsWith(oldContent || "")) {
      // 继续打字（如果没有在打字中）
      if (!timer && currentIndex < newContent.length) {
        typeNext();
      }
    } else {
      // 完全新的内容，重新开始
      if (timer) {
        clearTimeout(timer);
        timer = null;
      }
      currentIndex = 0;
      displayText.value = "";
      nextTick(() => typeNext());
    }
  },
  { immediate: true }
);

// 监听 streaming 状态变化
watch(
  () => props.streaming,
  (isStreaming) => {
    // 流式结束时，确保显示完整内容
    if (!isStreaming && currentIndex >= props.content.length) {
      emit("complete");
    }
  }
);

// 清理定时器
onUnmounted(() => {
  if (timer) {
    clearTimeout(timer);
  }
});
</script>

<template>
  <span class="typewriter">
    <slot :text="displayText">{{ displayText }}</slot>
    <span v-if="streaming || currentIndex < content.length" class="cursor"
      >▌</span
    >
  </span>
</template>

<style scoped>
.typewriter {
  display: inline;
}

.cursor {
  color: var(--el-color-primary);
  animation: blink 1s step-end infinite;
}

@keyframes blink {
  0%,
  50% {
    opacity: 1;
  }
  51%,
  100% {
    opacity: 0;
  }
}
</style>
