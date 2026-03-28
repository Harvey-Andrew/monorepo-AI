/**
 * 商品标题分类 Composable
 *
 * 管理商品标题分类相关状态和 API 调用
 */

import { ref } from "vue";
import { request } from "~/utils/request";

interface ClassificationResult {
  category: string;
}

interface BatchClassificationResult {
  categories: string[];
}

interface HistoryItem {
  text: string;
  category: string;
  timestamp: Date;
}

export function useProductClassification() {
  // 状态
  const inputText = ref("");
  const category = ref("");
  const isLoading = ref(false);
  const error = ref<string | null>(null);
  const history = ref<HistoryItem[]>([]);

  /**
   * 分类单个商品标题
   */
  async function classify(text?: string) {
    const textToClassify = text || inputText.value;

    if (!textToClassify.trim()) {
      error.value = "请输入商品标题";
      return;
    }

    isLoading.value = true;
    error.value = null;

    try {
      const res = await request.post<{ data: ClassificationResult }>(
        "/product-classification/predict",
        { text: textToClassify }
      );

      // API 返回格式: { code, data: { category }, message }
      const resultCategory = res.data?.category || "";
      category.value = resultCategory;

      // 添加到历史记录
      history.value.unshift({
        text: textToClassify,
        category: resultCategory,
        timestamp: new Date(),
      });

      // 限制历史记录数量
      if (history.value.length > 20) {
        history.value.pop();
      }
    } catch (e) {
      error.value = e instanceof Error ? e.message : "分类失败";
      throw e;
    } finally {
      isLoading.value = false;
    }
  }

  /**
   * 批量分类商品标题
   */
  async function classifyBatch(texts: string[]) {
    if (!texts.length) {
      error.value = "请输入商品标题";
      return [];
    }

    isLoading.value = true;
    error.value = null;

    try {
      const res = await request.post<BatchClassificationResult>(
        "/product-classification/predict/batch",
        { texts }
      );
      return res.categories;
    } catch (e) {
      error.value = e instanceof Error ? e.message : "批量分类失败";
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
    error.value = null;
  }

  /**
   * 清除历史记录
   */
  function clearHistory() {
    history.value = [];
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
    isLoading,
    error,
    history,

    // 方法
    classify,
    classifyBatch,
    clearResult,
    clearHistory,
    clearError,
  };
}
