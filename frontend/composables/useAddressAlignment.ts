/**
 * 地址对齐 Composable
 *
 * 提供地址序列标注和结构化提取功能的状态管理和 API 调用
 */

import { ref, reactive } from "vue";

interface AddressResult {
  prov: string | null;
  city: string | null;
  district: string | null;
  town: string | null;
  detail: string | null;
  name: string | null;
  phone: string | null;
}

interface TaggingResult {
  text: string;
  tags: string[];
}

interface HistoryItem extends AddressResult {
  text: string;
  timestamp: Date;
}

export function useAddressAlignment() {
  const inputText = ref("浙江省杭州市余杭区葛墩路27号楼傅婷15830444519");
  const result = ref<AddressResult | null>(null);
  const taggingResult = ref<TaggingResult | null>(null);
  const isLoading = ref(false);
  const error = ref<string | null>(null);
  const history = reactive<HistoryItem[]>([]);

  const config = useRuntimeConfig();
  const apiBase = config.public.pythonApiBase || "http://localhost:9000";

  /**
   * 调用地址对齐 API（包含数据库校验）
   */
  async function align(): Promise<AddressResult> {
    if (!inputText.value.trim()) {
      error.value = "请输入地址文本";
      throw new Error(error.value);
    }

    isLoading.value = true;
    error.value = null;

    try {
      const response = await fetch(`${apiBase}/api/address-alignment/align`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ text: inputText.value }),
      });

      const res = await response.json();

      if (res.code !== 200) {
        throw new Error(res.message || "地址对齐失败");
      }

      result.value = res.data;

      // 添加到历史记录
      history.unshift({
        text: inputText.value,
        ...res.data,
        timestamp: new Date(),
      });

      // 限制历史记录数量
      if (history.length > 10) {
        history.pop();
      }

      return res.data;
    } catch (e) {
      const errorMessage = e instanceof Error ? e.message : "请求失败";
      error.value = errorMessage;
      throw e;
    } finally {
      isLoading.value = false;
    }
  }

  /**
   * 调用地址提取 API（不使用数据库校验）
   */
  async function extract(): Promise<AddressResult> {
    if (!inputText.value.trim()) {
      error.value = "请输入地址文本";
      throw new Error(error.value);
    }

    isLoading.value = true;
    error.value = null;

    try {
      const response = await fetch(`${apiBase}/api/address-alignment/extract`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ text: inputText.value }),
      });

      const res = await response.json();

      if (res.code !== 200) {
        throw new Error(res.message || "地址提取失败");
      }

      result.value = res.data;
      return res.data;
    } catch (e) {
      const errorMessage = e instanceof Error ? e.message : "请求失败";
      error.value = errorMessage;
      throw e;
    } finally {
      isLoading.value = false;
    }
  }

  /**
   * 调用序列标注 API
   */
  async function tagging(): Promise<TaggingResult> {
    if (!inputText.value.trim()) {
      error.value = "请输入地址文本";
      throw new Error(error.value);
    }

    isLoading.value = true;
    error.value = null;

    try {
      const response = await fetch(`${apiBase}/api/address-alignment/tagging`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ text: inputText.value }),
      });

      const res = await response.json();

      if (res.code !== 200) {
        throw new Error(res.message || "序列标注失败");
      }

      taggingResult.value = res.data;
      return res.data;
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
    result.value = null;
    taggingResult.value = null;
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
    result,
    taggingResult,
    isLoading,
    error,
    history,
    // 方法
    align,
    extract,
    tagging,
    clearResult,
    clearHistory,
    clearError,
  };
}
