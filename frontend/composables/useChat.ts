/**
 * 聊天功能 Composable
 * 支持流式响应和本地存储
 */
/* global TextDecoder */
import type {
  ChatMessage,
  Conversation,
  SSEChunk,
  ChatRequest,
} from "~/types/chat";

const STORAGE_KEY = "ai-chat-conversations";

// 生成唯一ID
function generateId(): string {
  return Date.now().toString(36) + Math.random().toString(36).slice(2);
}

// 从消息生成会话标题
function generateTitle(content: string): string {
  return content.slice(0, 30) + (content.length > 30 ? "..." : "");
}

export function useChat() {
  // 所有会话
  const conversations = ref<Conversation[]>([]);
  // 当前活跃会话ID
  const activeConversationId = ref<string | null>(null);
  // 是否正在生成中
  const isGenerating = ref(false);
  // 输入框内容
  const inputText = ref("");

  // 当前会话
  const currentConversation = computed(() => {
    return conversations.value.find((c) => c.id === activeConversationId.value);
  });

  // 当前消息列表
  const messages = computed(() => {
    return currentConversation.value?.messages || [];
  });

  // 从本地存储加载
  function loadFromStorage() {
    if (import.meta.client) {
      const stored = localStorage.getItem(STORAGE_KEY);
      if (stored) {
        try {
          const data = JSON.parse(stored);
          conversations.value = data.conversations || [];
          activeConversationId.value = data.activeId || null;
        } catch {
          console.error("Failed to load chat history");
        }
      }
    }
  }

  // 保存到本地存储
  function saveToStorage() {
    if (import.meta.client) {
      localStorage.setItem(
        STORAGE_KEY,
        JSON.stringify({
          conversations: conversations.value,
          activeId: activeConversationId.value,
        })
      );
    }
  }

  // 创建新会话
  function createConversation(): Conversation {
    const now = Date.now();
    const conversation: Conversation = {
      id: generateId(),
      title: "新对话",
      messages: [],
      createdAt: now,
      updatedAt: now,
    };
    conversations.value.unshift(conversation);
    activeConversationId.value = conversation.id;
    saveToStorage();
    return conversation;
  }

  // 切换会话
  function switchConversation(id: string) {
    activeConversationId.value = id;
    saveToStorage();
  }

  // 删除会话
  function deleteConversation(id: string) {
    const index = conversations.value.findIndex((c) => c.id === id);
    if (index > -1) {
      conversations.value.splice(index, 1);
      // 如果删除的是当前会话，切换到第一个
      if (activeConversationId.value === id) {
        activeConversationId.value = conversations.value[0]?.id || null;
      }
      saveToStorage();
    }
  }

  // 发送消息
  async function sendMessage(content: string) {
    if (!content.trim() || isGenerating.value) return;

    // 确保有活跃会话
    let conversation = currentConversation.value;
    if (!conversation) {
      conversation = createConversation();
    }

    // 添加用户消息
    const userMessage: ChatMessage = {
      id: generateId(),
      role: "user",
      content: content.trim(),
      timestamp: Date.now(),
    };
    conversation.messages.push(userMessage);

    // 更新标题（如果是第一条消息）
    if (conversation.messages.length === 1) {
      conversation.title = generateTitle(content);
    }

    // 清空输入
    inputText.value = "";
    isGenerating.value = true;

    // 添加AI消息占位
    const aiMessage: ChatMessage = {
      id: generateId(),
      role: "assistant",
      content: "",
      timestamp: Date.now(),
      loading: true,
    };
    conversation.messages.push(aiMessage);
    saveToStorage();

    try {
      // 准备请求
      const requestBody: ChatRequest = {
        messages: conversation.messages
          .filter((m) => !m.loading)
          .map((m) => ({
            role: m.role,
            content: m.content,
          })),
        stream: true,
      };

      // 发送SSE请求
      const response = await fetch("/api/chat", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(requestBody),
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      // 读取流式响应
      const reader = response.body?.getReader();
      const decoder = new TextDecoder();

      if (!reader) {
        throw new Error("Response body is not readable");
      }

      while (true) {
        const { done, value } = await reader.read();
        if (done) break;

        const text = decoder.decode(value, { stream: true });
        const lines = text.split("\n");

        for (const line of lines) {
          if (line.startsWith("data: ")) {
            try {
              const data: SSEChunk = JSON.parse(line.slice(6));

              if (data.error) {
                aiMessage.content = `错误: ${data.error}`;
                break;
              }

              if (data.content) {
                aiMessage.content += data.content;
              }

              if (data.done) {
                aiMessage.loading = false;
              }
            } catch {
              // 忽略解析错误
            }
          }
        }
      }
    } catch (error) {
      console.error("Chat error:", error);
      aiMessage.content = `发送失败: ${error instanceof Error ? error.message : "未知错误"}`;
    } finally {
      aiMessage.loading = false;
      isGenerating.value = false;
      conversation.updatedAt = Date.now();
      saveToStorage();
    }
  }

  // 清空当前会话消息
  function clearMessages() {
    if (currentConversation.value) {
      currentConversation.value.messages = [];
      currentConversation.value.title = "新对话";
      saveToStorage();
    }
  }

  // 初始化加载
  onMounted(() => {
    loadFromStorage();
  });

  return {
    // 状态
    conversations,
    activeConversationId,
    currentConversation,
    messages,
    isGenerating,
    inputText,

    // 方法
    createConversation,
    switchConversation,
    deleteConversation,
    sendMessage,
    clearMessages,
    loadFromStorage,
  };
}
