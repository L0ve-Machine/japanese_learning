import { useState, useEffect } from 'react';
import { useLanguage } from '../contexts/LanguageContext';

interface TranslationState {
  originalText: string;
  translatedText: string | null;
  isLoading: boolean;
  error: string | null;
}

/**
 * テキスト翻訳用のカスタムフック
 */
export const useTranslation = (text: string, autoTranslate: boolean = false) => {
  const { currentLanguage, translateContent } = useLanguage();
  const [state, setState] = useState<TranslationState>({
    originalText: text,
    translatedText: null,
    isLoading: false,
    error: null
  });

  useEffect(() => {
    // テキストが変更されたら状態をリセット
    setState(prev => ({
      ...prev,
      originalText: text,
      translatedText: null,
      error: null
    }));

    // 自動翻訳が有効で、日本語以外の場合は翻訳
    if (autoTranslate && currentLanguage !== 'ja' && text) {
      translateText(text);
    }
  }, [text, currentLanguage, autoTranslate]);

  const translateText = async (textToTranslate?: string) => {
    const targetText = textToTranslate || text;
    if (!targetText) return;

    setState(prev => ({ ...prev, isLoading: true, error: null }));

    try {
      const translated = await translateContent(targetText);
      setState(prev => ({
        ...prev,
        translatedText: translated,
        isLoading: false
      }));
    } catch (error) {
      setState(prev => ({
        ...prev,
        error: error instanceof Error ? error.message : '翻訳エラーが発生しました',
        isLoading: false
      }));
    }
  };

  const resetTranslation = () => {
    setState({
      originalText: text,
      translatedText: null,
      isLoading: false,
      error: null
    });
  };

  return {
    originalText: state.originalText,
    translatedText: state.translatedText,
    isTranslated: !!state.translatedText,
    isLoading: state.isLoading,
    error: state.error,
    translate: translateText,
    reset: resetTranslation,
    displayText: state.translatedText || state.originalText
  };
};