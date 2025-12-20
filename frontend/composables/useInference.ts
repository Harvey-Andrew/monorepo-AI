/**
 * 通用推理 Hook
 *
 * 处理 Loading、Error 状态和类型安全的 API 调用
 */

import { ref, type Ref } from "vue";
import { request } from "~/utils/request";

export interface UseInferenceOptions<T> {
  /** API 路径 */
  url: string;
  /** 请求方法 */
  method?: "GET" | "POST";
  /** 成功回调 */
  onSuccess?: (data: T) => void;
  /** 错误回调 */
  onError?: (error: Error) => void;
}

export interface UseInferenceReturn<T> {
  data: Ref<T | null>;
  loading: Ref<boolean>;
  error: Ref<string | null>;
  execute: (formData?: FormData) => Promise<T | null>;
  reset: () => void;
}

export function useInference<T = any>(
  options: UseInferenceOptions<T>
): UseInferenceReturn<T> {
  const { url, method = "POST", onSuccess, onError } = options;

  const data = ref<T | null>(null) as Ref<T | null>;
  const loading = ref(false);
  const error = ref<string | null>(null);

  const execute = async (formData?: FormData): Promise<T | null> => {
    loading.value = true;
    error.value = null;

    try {
      let result: T;
      if (method === "POST" && formData) {
        result = await request.upload<T>(url, formData);
      } else if (method === "GET") {
        result = await request.get<T>(url);
      } else {
        result = await request.post<T>(url);
      }

      data.value = result;
      onSuccess?.(result);
      return result;
    } catch (e: any) {
      const errorMessage = e.message || "请求失败";
      error.value = errorMessage;
      onError?.(e);
      return null;
    } finally {
      loading.value = false;
    }
  };

  const reset = () => {
    data.value = null;
    loading.value = false;
    error.value = null;
  };

  return {
    data,
    loading,
    error,
    execute,
    reset,
  };
}
