/**
 * 图像处理业务逻辑 Composable
 *
 * 提供图片上传、去噪、分类、相似商品检索等功能
 */

import { request } from "~/utils/request";
import { useDebounceFn } from "@vueuse/core";
import type { 
  Result
} from "~/types/common";
import type { 
  DenoisingResponse, 
  ClassificationResponse, 
  SimilarityResponse 
} from "~/types/image-processing";
import { ElMessage } from "element-plus";
import { ref } from "vue";
import { DEBOUNCE_DELAY } from "~/utils/constants";

export const useImageProcess = () => {
  // 响应式状态
  const originalImage = ref<string>(""); // 原始图片 base64
  const noisyImage = ref<string>(""); // 噪声图片 base64
  const denoisedImage = ref<string>(""); // 去噪图片 base64
  const classificationResult = ref<string>(""); // 分类结果文本
  const similarImages = ref<string[]>([]); // 相似商品 URL 列表
  const isLoading = ref(false); // 加载状态
  const error = ref<string | null>(null); // 错误信息

  /**
   * 上传图片（转为 base64 预览）
   */
  const uploadImage = (file: File): Promise<void> => {
    return new Promise((resolve, reject) => {
      const reader = new FileReader();
      reader.onload = (e) => {
        originalImage.value = e.target?.result as string;
        // 清空之前的处理结果
        noisyImage.value = "";
        denoisedImage.value = "";
        classificationResult.value = "";
        similarImages.value = [];
        error.value = null;
        resolve();
      };
      reader.onerror = () => {
        error.value = "图片读取失败";
        reject(new Error("图片读取失败"));
      };
      reader.readAsDataURL(file);
    });
  };

  /**
   * Base64 转 Blob
   */
  const base64ToBlob = async (base64: string): Promise<Blob> => {
    const response = await fetch(base64);
    return response.blob();
  };

  /**
   * 图像去噪
   */
  const denoise = useDebounceFn(async () => {
    if (!originalImage.value) {
      error.value = "请先上传图片";
      return;
    }

    isLoading.value = true;
    error.value = null;

    try {
      const blob = await base64ToBlob(originalImage.value);
      const formData = new FormData();
      formData.append("image", blob, "image.png");

      const result = await request.upload<Result<DenoisingResponse>>(
        "/denoising",
        formData
      );

      if (result.data) {
        noisyImage.value = `data:image/png;base64,${result.data.noisy_img}`;
        denoisedImage.value = `data:image/png;base64,${result.data.denoised_image}`;
        ElMessage.success("去噪处理完成");
      }
    } finally {
      isLoading.value = false;
    }
  }, DEBOUNCE_DELAY);

  /**
   * 商品分类
   */
  const classify = useDebounceFn(async () => {
    if (!denoisedImage.value) {
      error.value = "请先进行去噪处理";
      return;
    }

    isLoading.value = true;
    error.value = null;

    try {
      const blob = await base64ToBlob(denoisedImage.value);
      const formData = new FormData();
      formData.append("image", blob, "image.png");

      const result = await request.upload<Result<ClassificationResponse>>(
        "/classification",
        formData
      );

      if (result.data) {
        classificationResult.value = result?.data?.result;
        ElMessage.success("分类处理完成");
      }
    }finally {
      isLoading.value = false;
    }
  }, DEBOUNCE_DELAY);

  /**
   * 相似商品检索
   * @param numImages 推荐数量，默认 10
   */
  const findSimilar = useDebounceFn(async (numImages: number = 10) => {
    if (!denoisedImage.value) {
      error.value = "请先进行去噪处理";
      return;
    }

    isLoading.value = true;
    error.value = null;

    try {
      const blob = await base64ToBlob(denoisedImage.value);
      const formData = new FormData();
      formData.append("image", blob, "image.png");
      formData.append("num_images", numImages.toString());

      const result = await request.upload<Result<SimilarityResponse>>(
        "/simimages",
        formData
      );

      if (result.data) {
        similarImages.value = result.data.image_urls;
        ElMessage.success(`找到 ${similarImages.value.length} 张相似图片`);
      }
    }  finally {
      isLoading.value = false;
    }
  }, DEBOUNCE_DELAY);

  /**
   * 清除错误信息
   */
  const clearError = () => {
    error.value = null;
  };

  return {
    // 状态
    originalImage,
    noisyImage,
    denoisedImage,
    classificationResult,
    similarImages,
    isLoading,
    error,
    // 方法
    uploadImage,
    denoise,
    classify,
    findSimilar,
    clearError,
  };
};
