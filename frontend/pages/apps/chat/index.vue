<script setup lang="ts">
/* eslint-disable no-undef */
/**
 * AI 聊天页面
 * 自定义实现：消息气泡 + 思考状态 + Markdown 渲染
 */
import {
  Delete,
  ChatDotRound,
  User,
  Position,
  DocumentCopy,
  Refresh,
} from "@element-plus/icons-vue";
import { ElMessage, ElMessageBox } from "element-plus";
import { marked } from "marked";
import type { ChatMessage } from "~/types/chat";

definePageMeta({
  layout: "default",
  title: "AI 助手",
});

// 配置 marked
marked.setOptions({
  breaks: true,
  gfm: true,
});

const {
  conversations,
  activeConversationId,
  messages,
  isGenerating,
  inputText,
  createConversation,
  switchConversation,
  deleteConversation,
  sendMessage,
} = useChat();

// 消息列表引用
const messagesRef = ref<HTMLElement | null>(null);

// 滚动到底部
function scrollToBottom() {
  nextTick(() => {
    if (messagesRef.value) {
      messagesRef.value.scrollTop = messagesRef.value.scrollHeight;
    }
  });
}

// 监听消息变化
watch(messages, () => scrollToBottom(), { deep: true });

// 处理发送
function handleSend() {
  if (!inputText.value.trim() || isGenerating.value) return;
  sendMessage(inputText.value);
}

// 键盘事件
function handleKeydown(e: KeyboardEvent) {
  if (e.key === "Enter" && !e.shiftKey) {
    e.preventDefault();
    handleSend();
  }
}

// 删除会话
function handleDelete(id: string, e: Event) {
  e.stopPropagation();
  ElMessageBox.confirm("确定要删除这个对话吗？", "删除确认", {
    confirmButtonText: "删除",
    cancelButtonText: "取消",
    type: "warning",
  })
    .then(() => {
      deleteConversation(id);
      ElMessage.success("已删除");
    })
    .catch(() => {});
}

// 格式化时间
function formatTime(timestamp: number): string {
  return new Date(timestamp).toLocaleString("zh-CN", {
    month: "2-digit",
    day: "2-digit",
    hour: "2-digit",
    minute: "2-digit",
  });
}

// 渲染 Markdown
function renderMarkdown(content: string): string {
  return content ? (marked(content) as string) : "";
}

// 复制内容
function copyContent(content: string) {
  navigator.clipboard.writeText(content);
  ElMessage.success("已复制到剪贴板");
}

// 重新生成（发送上一条用户消息）
function regenerate() {
  const lastUserMsg = [...messages.value]
    .reverse()
    .find((m) => m.role === "user");
  if (lastUserMsg) {
    sendMessage(lastUserMsg.content);
  }
}

// 状态判断
const isThinking = (msg: ChatMessage) => Boolean(msg.loading && !msg.content);
const isTyping = (msg: ChatMessage) =>
  Boolean(msg.role === "assistant" && msg.loading && msg.content);
</script>

<template>
  <div class="chat-page">
    <!-- 侧边栏 -->
    <aside class="chat-sidebar">
      <div class="chat-sidebar__header">
        <el-button
          type="primary"
          class="new-chat-btn"
          @click="createConversation"
        >
          <el-icon><ChatDotRound /></el-icon>
          新对话
        </el-button>
      </div>
      <div class="chat-sidebar__list">
        <template v-if="conversations.length > 0">
          <div
            v-for="conv in conversations"
            :key="conv.id"
            class="conversation-item"
            :class="{ active: conv.id === activeConversationId }"
            @click="switchConversation(conv.id)"
          >
            <span class="conversation-item__title">{{ conv.title }}</span>
            <el-icon
              class="conversation-item__delete"
              @click="handleDelete(conv.id, $event)"
            >
              <Delete />
            </el-icon>
          </div>
        </template>
        <div v-else class="chat-sidebar__empty">暂无对话</div>
      </div>
    </aside>

    <!-- 主聊天区 -->
    <main class="chat-main">
      <div ref="messagesRef" class="chat-messages">
        <template v-if="messages.length > 0">
          <div
            v-for="msg in messages"
            :key="msg.id"
            class="message-row"
            :class="`message-row--${msg.role}`"
          >
            <!-- 头像 -->
            <div class="message-avatar" :class="`message-avatar--${msg.role}`">
              <el-icon v-if="msg.role === 'user'"><User /></el-icon>
              <span v-else>🤖</span>
            </div>

            <!-- 内容区 -->
            <div class="message-body">
              <div class="message-meta">
                <span class="message-name">{{
                  msg.role === "user" ? "我" : "AI 助手"
                }}</span>
                <span class="message-time">{{
                  formatTime(msg.timestamp)
                }}</span>
              </div>

              <div
                class="message-bubble"
                :class="`message-bubble--${msg.role}`"
              >
                <!-- 思考状态 -->
                <div v-if="isThinking(msg)" class="thinking-animation">
                  <span>思</span><span>考</span><span>中</span> <span>.</span
                  ><span>.</span><span>.</span>
                </div>
                <!-- AI 消息 -->
                <template v-else-if="msg.role === 'assistant'">
                  <!-- 正在生成中：使用打字机效果 -->
                  <Typewriter
                    v-if="msg.loading"
                    :content="msg.content"
                    :speed="20"
                    :streaming="true"
                    @update="scrollToBottom"
                  >
                    <template #default="{ text }">
                      <div
                        class="markdown-content"
                        v-html="renderMarkdown(text)"
                      ></div>
                    </template>
                  </Typewriter>
                  <!-- 已完成：直接显示 -->
                  <div
                    v-else
                    class="markdown-content"
                    v-html="renderMarkdown(msg.content)"
                  ></div>
                </template>
                <!-- 用户消息 -->
                <template v-else>
                  <div class="user-text">{{ msg.content }}</div>
                </template>
              </div>

              <!-- AI 消息操作按钮 -->
              <div
                v-if="msg.role === 'assistant' && msg.content && !msg.loading"
                class="message-actions"
              >
                <el-button
                  size="small"
                  :icon="DocumentCopy"
                  circle
                  @click="copyContent(msg.content)"
                />
                <el-button
                  size="small"
                  :icon="Refresh"
                  circle
                  @click="regenerate"
                />
              </div>
            </div>
          </div>
        </template>
        <div v-else class="chat-empty">
          <div class="chat-empty__icon">🤖</div>
          <div class="chat-empty__text">开始一段新对话吧</div>
        </div>
      </div>

      <!-- 输入区 -->
      <div class="chat-input-area">
        <div class="chat-input-wrapper">
          <el-input
            v-model="inputText"
            type="textarea"
            :rows="2"
            placeholder="输入消息，Enter 发送，Shift+Enter 换行"
            :disabled="isGenerating"
            @keydown="handleKeydown"
          />
          <el-button
            type="primary"
            :loading="isGenerating"
            :disabled="!inputText.trim()"
            @click="handleSend"
          >
            <el-icon v-if="!isGenerating"><Position /></el-icon>
            {{ isGenerating ? "生成中" : "发送" }}
          </el-button>
        </div>
        <div class="chat-input-hint">AI 可能会产生不准确的回答，请注意甄别</div>
      </div>
    </main>
  </div>
</template>

<style lang="scss" scoped>
.chat-page {
  display: flex;
  height: calc(100vh - 60px);
  background: var(--el-bg-color-page);
}

// 侧边栏
.chat-sidebar {
  width: 260px;
  background: var(--el-bg-color);
  border-right: 1px solid var(--el-border-color-light);
  display: flex;
  flex-direction: column;

  &__header {
    padding: 16px;
    border-bottom: 1px solid var(--el-border-color-light);
  }

  .new-chat-btn {
    width: 100%;
  }

  &__list {
    flex: 1;
    overflow-y: auto;
    padding: 8px;
  }

  &__empty {
    text-align: center;
    color: var(--el-text-color-placeholder);
    padding: 40px 16px;
  }
}

.conversation-item {
  display: flex;
  align-items: center;
  padding: 12px;
  border-radius: 8px;
  cursor: pointer;
  margin-bottom: 4px;
  transition: background 0.2s;

  &:hover {
    background: var(--el-fill-color-light);
  }

  &.active {
    background: var(--el-color-primary-light-9);
  }

  &__title {
    flex: 1;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
    font-size: 14px;
  }

  &__delete {
    opacity: 0;
    color: var(--el-text-color-secondary);
    transition: opacity 0.2s;

    &:hover {
      color: var(--el-color-danger);
    }
  }

  &:hover &__delete {
    opacity: 1;
  }
}

// 主区域
.chat-main {
  flex: 1;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.chat-messages {
  flex: 1;
  overflow-y: auto;
  padding: 24px;
}

// 消息行
.message-row {
  display: flex;
  gap: 12px;
  margin-bottom: 24px;

  &--user {
    flex-direction: row-reverse;

    .message-body {
      align-items: flex-end;
    }

    .message-meta {
      flex-direction: row-reverse;
    }
  }
}

.message-avatar {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 18px;
  flex-shrink: 0;

  &--user {
    background: linear-gradient(135deg, #667eea, #764ba2);
    color: white;
  }

  &--assistant {
    background: linear-gradient(135deg, #f093fb, #f5576c);
  }
}

.message-body {
  display: flex;
  flex-direction: column;
  gap: 6px;
  max-width: 70%;
}

.message-meta {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 13px;

  .message-name {
    color: var(--el-text-color-secondary);
    font-weight: 500;
  }

  .message-time {
    color: var(--el-text-color-placeholder);
    font-size: 12px;
  }
}

.message-bubble {
  padding: 12px 16px;
  border-radius: 16px;
  line-height: 1.6;

  &--user {
    background: linear-gradient(135deg, #667eea, #764ba2);
    color: white;
    border-bottom-right-radius: 4px;
  }

  &--assistant {
    background: var(--el-fill-color-light);
    border-bottom-left-radius: 4px;
  }
}

.user-text {
  white-space: pre-wrap;
}

.message-actions {
  display: flex;
  gap: 8px;
  margin-top: 4px;

  :deep(.el-button) {
    opacity: 0.5;
    &:hover {
      opacity: 1;
    }
  }
}

// 思考动画
.thinking-animation {
  color: var(--el-color-primary);

  span {
    display: inline-block;
    animation: bounce 1.4s ease infinite;
  }

  @for $i from 1 through 6 {
    span:nth-child(#{$i}) {
      animation-delay: #{($i - 1) * 0.15}s;
    }
  }
}

@keyframes bounce {
  0%,
  100% {
    transform: translateY(2px);
  }
  50% {
    transform: translateY(-2px);
  }
}

.typing-cursor {
  color: var(--el-color-primary);
  animation: blink 1s infinite;
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

// Markdown 内容
.markdown-content {
  :deep(p) {
    margin: 8px 0;
  }
  :deep(h1, h2, h3) {
    margin: 12px 0 8px;
    font-weight: 600;
  }
  :deep(code) {
    background: rgba(0, 0, 0, 0.08);
    padding: 2px 6px;
    border-radius: 4px;
    font-family: Consolas, Monaco, monospace;
  }
  :deep(pre) {
    background: var(--el-fill-color-darker);
    padding: 12px;
    border-radius: 8px;
    overflow-x: auto;
    code {
      background: none;
    }
  }
  :deep(ul, ol) {
    padding-left: 20px;
  }
  :deep(blockquote) {
    border-left: 3px solid var(--el-color-primary);
    padding-left: 12px;
    color: var(--el-text-color-secondary);
  }
}

// 空状态
.chat-empty {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100%;
  color: var(--el-text-color-placeholder);

  &__icon {
    font-size: 64px;
    margin-bottom: 16px;
  }
  &__text {
    font-size: 16px;
  }
}

// 输入区
.chat-input-area {
  padding: 16px 24px;
  border-top: 1px solid var(--el-border-color-light);
  background: var(--el-bg-color);
}

.chat-input-wrapper {
  display: flex;
  gap: 12px;

  :deep(.el-textarea__inner) {
    resize: none;
    border-radius: 12px;
  }

  .el-button {
    height: auto;
    align-self: flex-end;
    padding: 12px 24px;
  }
}

.chat-input-hint {
  text-align: center;
  font-size: 12px;
  color: var(--el-text-color-placeholder);
  margin-top: 8px;
}
</style>
