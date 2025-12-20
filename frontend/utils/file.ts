/**
 * Base64 转 Blob
 * @param base64 Base64 字符串
 * @returns Blob 对象
 */
export const base64ToBlob = async (base64: string): Promise<Blob> => {
  const response = await fetch(base64);
  return response.blob();
};
