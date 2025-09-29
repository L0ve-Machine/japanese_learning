import React, { createContext, useContext, useState, useEffect, ReactNode } from 'react';

export type LanguageCode = 'ja' | 'en' | 'vi' | 'id' | 'zh' | 'ko' | 'th' | 'my';

interface Language {
  code: LanguageCode;
  name: string;
  nativeName: string;
  flag: string;
}

export const languages: Language[] = [
  { code: 'ja', name: 'Japanese', nativeName: '日本語', flag: '🇯🇵' },
  { code: 'en', name: 'English', nativeName: 'English', flag: '🇬🇧' },
  { code: 'vi', name: 'Vietnamese', nativeName: 'Tiếng Việt', flag: '🇻🇳' },
  { code: 'id', name: 'Indonesian', nativeName: 'Bahasa Indonesia', flag: '🇮🇩' },
  { code: 'zh', name: 'Chinese', nativeName: '中文', flag: '🇨🇳' },
  { code: 'ko', name: 'Korean', nativeName: '한국어', flag: '🇰🇷' },
  { code: 'th', name: 'Thai', nativeName: 'ไทย', flag: '🇹🇭' },
  { code: 'my', name: 'Myanmar', nativeName: 'မြန်မာ', flag: '🇲🇲' }
];

interface LanguageContextType {
  currentLanguage: LanguageCode;
  setLanguage: (language: LanguageCode) => void;
  getTranslation: (key: string) => string;
  translateContent: (content: string, targetLang?: LanguageCode) => Promise<string>;
}

// UI翻訳用の静的辞書
const translations: Record<LanguageCode, Record<string, string>> = {
  ja: {
    'nav.dashboard': 'ダッシュボード',
    'nav.past_exams': '過去問題',
    'nav.subjects': '科目学習',
    'nav.vocabulary': '単語帳',
    'nav.flashcards': '暗記カード',
    'nav.videos': '解説動画',
    'nav.subscription': 'プラン',
    'nav.profile': 'プロフィール',
    'nav.logout': 'ログアウト',
    'common.welcome': 'ようこそ',
    'common.loading': '読み込み中...',
    'common.error': 'エラーが発生しました',
    'common.save': '保存',
    'common.cancel': 'キャンセル',
    'common.search': '検索',
    'common.filter': 'フィルター',
    'subscription.required': 'プレミアムプランの登録が必要です',
    'subscription.upgrade': 'アップグレード'
  },
  en: {
    'nav.dashboard': 'Dashboard',
    'nav.past_exams': 'Past Exams',
    'nav.subjects': 'Subjects',
    'nav.vocabulary': 'Vocabulary',
    'nav.flashcards': 'Flashcards',
    'nav.videos': 'Videos',
    'nav.subscription': 'Plans',
    'nav.profile': 'Profile',
    'nav.logout': 'Logout',
    'common.welcome': 'Welcome',
    'common.loading': 'Loading...',
    'common.error': 'An error occurred',
    'common.save': 'Save',
    'common.cancel': 'Cancel',
    'common.search': 'Search',
    'common.filter': 'Filter',
    'subscription.required': 'Premium subscription required',
    'subscription.upgrade': 'Upgrade'
  },
  vi: {
    'nav.dashboard': 'Bảng điều khiển',
    'nav.past_exams': 'Đề thi cũ',
    'nav.subjects': 'Môn học',
    'nav.vocabulary': 'Từ vựng',
    'nav.flashcards': 'Thẻ ghi nhớ',
    'nav.videos': 'Video',
    'nav.subscription': 'Gói dịch vụ',
    'nav.profile': 'Hồ sơ',
    'nav.logout': 'Đăng xuất',
    'common.welcome': 'Chào mừng',
    'common.loading': 'Đang tải...',
    'common.error': 'Đã xảy ra lỗi',
    'common.save': 'Lưu',
    'common.cancel': 'Hủy',
    'common.search': 'Tìm kiếm',
    'common.filter': 'Lọc',
    'subscription.required': 'Yêu cầu đăng ký Premium',
    'subscription.upgrade': 'Nâng cấp'
  },
  id: {
    'nav.dashboard': 'Dasbor',
    'nav.past_exams': 'Ujian Sebelumnya',
    'nav.subjects': 'Mata Pelajaran',
    'nav.vocabulary': 'Kosakata',
    'nav.flashcards': 'Kartu Memori',
    'nav.videos': 'Video',
    'nav.subscription': 'Paket',
    'nav.profile': 'Profil',
    'nav.logout': 'Keluar',
    'common.welcome': 'Selamat datang',
    'common.loading': 'Memuat...',
    'common.error': 'Terjadi kesalahan',
    'common.save': 'Simpan',
    'common.cancel': 'Batal',
    'common.search': 'Cari',
    'common.filter': 'Filter',
    'subscription.required': 'Diperlukan langganan Premium',
    'subscription.upgrade': 'Tingkatkan'
  },
  zh: {
    'nav.dashboard': '仪表板',
    'nav.past_exams': '历年试题',
    'nav.subjects': '科目学习',
    'nav.vocabulary': '词汇表',
    'nav.flashcards': '记忆卡',
    'nav.videos': '视频',
    'nav.subscription': '套餐',
    'nav.profile': '个人资料',
    'nav.logout': '退出',
    'common.welcome': '欢迎',
    'common.loading': '加载中...',
    'common.error': '发生错误',
    'common.save': '保存',
    'common.cancel': '取消',
    'common.search': '搜索',
    'common.filter': '筛选',
    'subscription.required': '需要Premium订阅',
    'subscription.upgrade': '升级'
  },
  ko: {
    'nav.dashboard': '대시보드',
    'nav.past_exams': '기출문제',
    'nav.subjects': '과목 학습',
    'nav.vocabulary': '단어장',
    'nav.flashcards': '암기 카드',
    'nav.videos': '동영상',
    'nav.subscription': '요금제',
    'nav.profile': '프로필',
    'nav.logout': '로그아웃',
    'common.welcome': '환영합니다',
    'common.loading': '로딩 중...',
    'common.error': '오류가 발생했습니다',
    'common.save': '저장',
    'common.cancel': '취소',
    'common.search': '검색',
    'common.filter': '필터',
    'subscription.required': '프리미엄 구독이 필요합니다',
    'subscription.upgrade': '업그레이드'
  },
  th: {
    'nav.dashboard': 'แดชบอร์ด',
    'nav.past_exams': 'ข้อสอบเก่า',
    'nav.subjects': 'วิชาเรียน',
    'nav.vocabulary': 'คำศัพท์',
    'nav.flashcards': 'บัตรคำ',
    'nav.videos': 'วิดีโอ',
    'nav.subscription': 'แพ็คเกจ',
    'nav.profile': 'โปรไฟล์',
    'nav.logout': 'ออกจากระบบ',
    'common.welcome': 'ยินดีต้อนรับ',
    'common.loading': 'กำลังโหลด...',
    'common.error': 'เกิดข้อผิดพลาด',
    'common.save': 'บันทึก',
    'common.cancel': 'ยกเลิก',
    'common.search': 'ค้นหา',
    'common.filter': 'กรอง',
    'subscription.required': 'ต้องสมัครแพ็คเกจพรีเมียม',
    'subscription.upgrade': 'อัพเกรด'
  },
  my: {
    'nav.dashboard': 'ဒက်ရှ်ဘုတ်',
    'nav.past_exams': 'စာမေးပွဲဟောင်းများ',
    'nav.subjects': 'ဘာသာရပ်များ',
    'nav.vocabulary': 'ဝေါဟာရများ',
    'nav.flashcards': 'မှတ်ကတ်များ',
    'nav.videos': 'ဗီဒီယိုများ',
    'nav.subscription': 'အစီအစဉ်များ',
    'nav.profile': 'ပရိုဖိုင်',
    'nav.logout': 'ထွက်ရန်',
    'common.welcome': 'ကြိုဆိုပါတယ်',
    'common.loading': 'ခဏစောင့်ပါ...',
    'common.error': 'အမှားတစ်ခု ဖြစ်ပွားခဲ့သည်',
    'common.save': 'သိမ်းဆည်းရန်',
    'common.cancel': 'ပယ်ဖျက်ရန်',
    'common.search': 'ရှာဖွေရန်',
    'common.filter': 'စစ်ထုတ်ရန်',
    'subscription.required': 'Premium အစီအစဉ် လိုအပ်ပါသည်',
    'subscription.upgrade': 'အဆင့်မြှင့်ရန်'
  }
};

const LanguageContext = createContext<LanguageContextType | undefined>(undefined);

export const useLanguage = () => {
  const context = useContext(LanguageContext);
  if (!context) {
    throw new Error('useLanguage must be used within LanguageProvider');
  }
  return context;
};

interface LanguageProviderProps {
  children: ReactNode;
}

export const LanguageProvider: React.FC<LanguageProviderProps> = ({ children }) => {
  const [currentLanguage, setCurrentLanguage] = useState<LanguageCode>(() => {
    const saved = localStorage.getItem('preferredLanguage');
    return (saved as LanguageCode) || 'ja';
  });

  const setLanguage = (language: LanguageCode) => {
    setCurrentLanguage(language);
    localStorage.setItem('preferredLanguage', language);
  };

  const getTranslation = (key: string): string => {
    return translations[currentLanguage]?.[key] || translations['ja'][key] || key;
  };

  const translateContent = async (content: string, targetLang?: LanguageCode): Promise<string> => {
    const targetLanguage = targetLang || currentLanguage;

    if (targetLanguage === 'ja') {
      return content; // 日本語の場合は翻訳不要
    }

    try {
      const response = await fetch('/api/translations/translate/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${localStorage.getItem('token')}`
        },
        body: JSON.stringify({
          text: content,
          target_language: targetLanguage,
          source_language: 'ja'
        })
      });

      if (response.ok) {
        const data = await response.json();
        return data.translated_text || content;
      }
    } catch (error) {
      console.error('Translation failed:', error);
    }

    return content; // 翻訳失敗時は元のテキストを返す
  };

  useEffect(() => {
    // HTMLのlang属性を更新
    document.documentElement.lang = currentLanguage;
  }, [currentLanguage]);

  return (
    <LanguageContext.Provider
      value={{
        currentLanguage,
        setLanguage,
        getTranslation,
        translateContent
      }}
    >
      {children}
    </LanguageContext.Provider>
  );
};