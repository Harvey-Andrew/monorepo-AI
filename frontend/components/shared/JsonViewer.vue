<template>
  <div class="json-viewer">
    <div v-if="title" class="viewer-header">
      <span class="viewer-title">{{ title }}</span>
      <el-button
        v-if="copyable"
        type="primary"
        link
        size="small"
        @click="handleCopy"
      >
        复制
      </el-button>
    </div>
    <pre class="viewer-content"><code>{{ formattedData }}</code></pre>
  </div>
</template>

<script setup lang="ts">
import { computed } from "vue";
import { ElMessage } from "element-plus";

interface Props {
  data: any;
  title?: string;
  indent?: number;
  copyable?: boolean;
}

const props = withDefaults(defineProps<Props>(), {
  title: "",
  indent: 2,
  copyable: true,
});

const formattedData = computed(() => {
  try {
    return JSON.stringify(props.data, null, props.indent);
  } catch {
    return String(props.data);
  }
});

const handleCopy = async () => {
  try {
    await navigator.clipboard.writeText(formattedData.value);
    ElMessage.success("已复制到剪贴板");
  } catch {
    ElMessage.error("复制失败");
  }
};
</script>

<style lang="scss" scoped>
.json-viewer {
  background: var(--el-fill-color-darker);
  border-radius: 8px;
  overflow: hidden;
}

.viewer-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 8px 12px;
  background: var(--el-fill-color-dark);
  border-bottom: 1px solid var(--el-border-color);
}

.viewer-title {
  font-size: 12px;
  font-weight: 500;
  color: var(--el-text-color-secondary);
}

.viewer-content {
  margin: 0;
  padding: 12px;
  font-family: "Fira Code", "Consolas", monospace;
  font-size: 12px;
  line-height: 1.5;
  color: var(--el-text-color-regular);
  overflow-x: auto;
}
</style>
