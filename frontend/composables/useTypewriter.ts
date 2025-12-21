/**
 * 打字机效果 Composable
 * 用于在前端模拟逐字输出效果
 */

export interface TypewriterOptions {
  /** 每个字符的延迟时间（毫秒） */
  speed?: number;
  /** 完成后的回调 */
  onComplete?: () => void;
  /** 每次更新后的回调 */
  onUpdate?: (text: string) => void;
}

export function useTypewriter(options: TypewriterOptions = {}) {
  const { speed = 30, onComplete, onUpdate } = options;

  // 当前显示的文本
  const displayText = ref("");
  // 完整的目标文本
  const fullText = ref("");
  // 是否正在打字中
  const isTyping = ref(false);
  // 定时器ID
  let timerId: ReturnType<typeof setTimeout> | null = null;
  // 当前字符索引
  let currentIndex = 0;

  // 开始打字机效果
  function start(text: string) {
    // 停止之前的打字
    stop();

    fullText.value = text;
    displayText.value = "";
    currentIndex = 0;
    isTyping.value = true;

    typeNextChar();
  }

  // 打下一个字符
  function typeNextChar() {
    if (currentIndex < fullText.value.length) {
      displayText.value += fullText.value[currentIndex];
      currentIndex++;
      onUpdate?.(displayText.value);

      timerId = setTimeout(typeNextChar, speed);
    } else {
      // 完成
      isTyping.value = false;
      onComplete?.();
    }
  }

  // 追加内容（用于流式响应）
  function append(text: string) {
    fullText.value += text;

    // 如果没有在打字，开始打字
    if (!isTyping.value && currentIndex < fullText.value.length) {
      isTyping.value = true;
      typeNextChar();
    }
  }

  // 立即显示全部内容
  function complete() {
    stop();
    displayText.value = fullText.value;
    currentIndex = fullText.value.length;
    isTyping.value = false;
    onComplete?.();
  }

  // 停止打字
  function stop() {
    if (timerId) {
      clearTimeout(timerId);
      timerId = null;
    }
    isTyping.value = false;
  }

  // 重置
  function reset() {
    stop();
    displayText.value = "";
    fullText.value = "";
    currentIndex = 0;
  }

  // 组件卸载时清理
  onUnmounted(() => {
    stop();
  });

  return {
    displayText,
    fullText,
    isTyping,
    start,
    append,
    complete,
    stop,
    reset,
  };
}
