/**
 * 聊天相关类型定义
 */

// 聊天消息
export interface ChatMessage {
  id: string
  role: 'user' | 'assistant' | 'system'
  content: string
  timestamp: number
  loading?: boolean // 是否正在加载中
}

// 会话
export interface Conversation {
  id: string
  title: string
  messages: ChatMessage[]
  createdAt: number
  updatedAt: number
}

// SSE响应数据
export interface SSEChunk {
  content?: string
  error?: string
  done: boolean
}

// 聊天请求
export interface ChatRequest {
  messages: Array<{
    role: 'user' | 'assistant' | 'system'
    content: string
  }>
  stream?: boolean
}
