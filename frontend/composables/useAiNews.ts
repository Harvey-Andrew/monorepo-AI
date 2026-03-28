/**
 * AI 新闻分析 Composable
 *
 * 提供新闻分类和摘要生成功能的状态管理和 API 调用
 */

import { ref, reactive } from "vue";

interface HistoryItem {
  text: string;
  category: string;
  summary: string;
  timestamp: Date;
}

interface AnalyzeResult {
  category: string;
  summary: string;
}

export function useAiNews() {
  const inputText =
    ref(`🔮 苹果与谷歌达成多年合作协议，🤖 Gemini 模型将为 Siri 提供 AI 支持

苹果与 Google 宣布达成多年合作，下一代 Apple Foundation Models 将基于 Google Gemini 模型及云技术，为今年推出的 Apple 智能功能提供支持，包括更个性化的 Siri。苹果表示，相关功能仍运行于设备端与私有云计算，并维持既有隐私标准。`);
  const category = ref("");
  const summary = ref("");
  const isLoading = ref(false);
  const error = ref<string | null>(null);
  const history = reactive<HistoryItem[]>([]);

  const config = useRuntimeConfig();
  const apiBase = config.public.pythonApiBase || "http://localhost:9000";

  /**
   * 调用综合分析 API
   */
  async function analyze(): Promise<AnalyzeResult> {
    if (!inputText.value.trim()) {
      error.value = "请输入新闻文本";
      throw new Error(error.value);
    }

    isLoading.value = true;
    error.value = null;

    try {
      const response = await fetch(`${apiBase}/api/ai-news/analyze`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ text: inputText.value }),
      });

      const result = await response.json();

      if (result.code !== 200) {
        throw new Error(result.message || "分析失败");
      }

      category.value = result.data.category;
      summary.value = result.data.summary;

      // 添加到历史记录
      history.unshift({
        text:
          inputText.value.length > 100
            ? inputText.value.substring(0, 100) + "..."
            : inputText.value,
        category: result.data.category,
        summary: result.data.summary,
        timestamp: new Date(),
      });

      // 限制历史记录数量
      if (history.length > 10) {
        history.pop();
      }

      return result.data;
    } catch (e) {
      const errorMessage = e instanceof Error ? e.message : "请求失败";
      error.value = errorMessage;
      throw e;
    } finally {
      isLoading.value = false;
    }
  }

  /**
   * 调用分类 API
   */
  async function classify(): Promise<string> {
    if (!inputText.value.trim()) {
      error.value = "请输入新闻文本";
      throw new Error(error.value);
    }

    isLoading.value = true;
    error.value = null;

    try {
      const response = await fetch(`${apiBase}/api/ai-news/classify`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ text: inputText.value }),
      });

      const result = await response.json();

      if (result.code !== 200) {
        throw new Error(result.message || "分类失败");
      }

      category.value = result.data.category;
      return result.data.category;
    } catch (e) {
      const errorMessage = e instanceof Error ? e.message : "请求失败";
      error.value = errorMessage;
      throw e;
    } finally {
      isLoading.value = false;
    }
  }

  /**
   * 调用摘要 API
   */
  async function summarize(): Promise<string> {
    if (!inputText.value.trim()) {
      error.value = "请输入新闻文本";
      throw new Error(error.value);
    }

    isLoading.value = true;
    error.value = null;

    try {
      const response = await fetch(`${apiBase}/api/ai-news/summarize`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ text: inputText.value }),
      });

      const result = await response.json();

      if (result.code !== 200) {
        throw new Error(result.message || "摘要生成失败");
      }

      summary.value = result.data.summary;
      return result.data.summary;
    } catch (e) {
      const errorMessage = e instanceof Error ? e.message : "请求失败";
      error.value = errorMessage;
      throw e;
    } finally {
      isLoading.value = false;
    }
  }

  /**
   * 清除结果
   */
  function clearResult() {
    category.value = "";
    summary.value = "";
  }

  /**
   * 清除历史记录
   */
  function clearHistory() {
    history.splice(0, history.length);
  }

  /**
   * 清除错误
   */
  function clearError() {
    error.value = null;
  }

  return {
    // 状态
    inputText,
    category,
    summary,
    isLoading,
    error,
    history,
    // 方法
    analyze,
    classify,
    summarize,
    clearResult,
    clearHistory,
    clearError,
  };
}
