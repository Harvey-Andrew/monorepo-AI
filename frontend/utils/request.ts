/**
 * Axios 请求工具
 */

import axios, { type AxiosInstance, type AxiosRequestConfig } from "axios";
import { ApiCode } from "~/types/api";
import { ElMessage } from "element-plus";

const createAxiosInstance = (): AxiosInstance => {
  const instance = axios.create({
    baseURL: "/api",
    timeout: 60000,
    headers: {
      "Content-Type": "application/json",
    },
  });

  instance.interceptors.response.use(
    (response) => {
      const res = response.data;
      // 如果响应是二进制数据或没有 code 字段，直接返回
      if (
        res instanceof Blob ||
        res instanceof ArrayBuffer ||
        !res ||
        typeof res !== "object" ||
        !("code" in res)
      ) {
        return response;
      }

      // 统一处理业务错误
      if (res.code !== ApiCode.SUCCESS) {
        const message = res.message || "请求失败";
        if (import.meta.client) {
          ElMessage.error(message);
        }
        const error = new Error(message);
        // @ts-ignore
        error.data = res.data;
        return Promise.reject(error);
      }

      return response;
    },
    (error) => {
      const message =
        error.response?.data?.message ||
        error.response?.data?.detail ||
        error.message ||
        "请求失败";
      
      if (import.meta.client) {
        ElMessage.error(message);
      }
      return Promise.reject(new Error(message));
    }
  );

  return instance;
};

export const http = createAxiosInstance();

export const request = {
  get<T = any>(url: string, config?: AxiosRequestConfig): Promise<T> {
    return http.get(url, config).then((res) => res.data);
  },

  post<T = any>(
    url: string,
    data?: any,
    config?: AxiosRequestConfig
  ): Promise<T> {
    return http.post(url, data, config).then((res) => res.data);
  },

  upload<T = any>(url: string, formData: FormData): Promise<T> {
    return http
      .post(url, formData, {
        headers: { "Content-Type": "multipart/form-data" },
      })
      .then((res) => res.data);
  },
};

export default http;
