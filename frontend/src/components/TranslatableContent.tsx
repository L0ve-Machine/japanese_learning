import React, { useState, useEffect } from 'react';
import { Box, IconButton, Tooltip, CircularProgress } from '@mui/material';
import { Translate, Close } from '@mui/icons-material';
import { useLanguage } from '../contexts/LanguageContext';

interface TranslatableContentProps {
  children: React.ReactNode;
  originalText?: string;
  allowTranslate?: boolean;
}

/**
 * コンテンツに翻訳ボタンを追加するラッパーコンポーネント
 */
const TranslatableContent: React.FC<TranslatableContentProps> = ({
  children,
  originalText,
  allowTranslate = true
}) => {
  const { currentLanguage, translateContent } = useLanguage();
  const [isTranslated, setIsTranslated] = useState(false);
  const [translatedText, setTranslatedText] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(false);

  const textContent = originalText || (typeof children === 'string' ? children : '');

  useEffect(() => {
    // 言語が変更されたら翻訳をリセット
    setIsTranslated(false);
    setTranslatedText(null);
  }, [currentLanguage]);

  const handleTranslate = async () => {
    if (!textContent) return;

    if (isTranslated) {
      setIsTranslated(false);
    } else {
      setIsLoading(true);
      try {
        const translated = await translateContent(textContent);
        setTranslatedText(translated);
        setIsTranslated(true);
      } catch (error) {
        console.error('Translation failed:', error);
      } finally {
        setIsLoading(false);
      }
    }
  };

  // 日本語の場合や翻訳不可の場合は翻訳ボタンを表示しない
  if (!allowTranslate || currentLanguage === 'ja' || !textContent) {
    return <>{children}</>;
  }

  return (
    <Box sx={{ position: 'relative', display: 'inline-block' }}>
      <Box sx={{ pr: 4 }}>
        {isTranslated && translatedText ? translatedText : children}
      </Box>
      <Tooltip title={isTranslated ? '元のテキストを表示' : '翻訳'}>
        <IconButton
          size="small"
          onClick={handleTranslate}
          disabled={isLoading}
          sx={{
            position: 'absolute',
            top: 0,
            right: 0,
            p: 0.5,
            backgroundColor: 'background.paper',
            '&:hover': {
              backgroundColor: 'action.hover'
            }
          }}
        >
          {isLoading ? (
            <CircularProgress size={16} />
          ) : isTranslated ? (
            <Close fontSize="small" />
          ) : (
            <Translate fontSize="small" />
          )}
        </IconButton>
      </Tooltip>
    </Box>
  );
};

export default TranslatableContent;