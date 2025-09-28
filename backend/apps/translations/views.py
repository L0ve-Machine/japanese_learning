from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.core.cache import cache
from django.conf import settings
import hashlib
import json

from .models import TranslationCache, UserLanguagePreference
from .services import TranslationService

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def translate_text(request):
    """テキスト翻訳API"""
    text = request.data.get('text', '')
    target_language = request.data.get('target_language', 'en')
    source_language = request.data.get('source_language', 'ja')

    if not text:
        return Response({'error': 'Text is required'}, status=status.HTTP_400_BAD_REQUEST)

    # キャッシュキー生成
    cache_key = f"translation:{hashlib.md5(f'{text}:{source_language}:{target_language}'.encode()).hexdigest()}"

    # キャッシュから取得
    cached_translation = cache.get(cache_key)
    if cached_translation:
        return Response({
            'translated_text': cached_translation,
            'source_language': source_language,
            'target_language': target_language,
            'from_cache': True
        })

    # DBキャッシュから取得
    try:
        db_cache = TranslationCache.objects.get(
            original_text=text,
            source_language=source_language,
            target_language=target_language
        )
        # メモリキャッシュに保存
        cache.set(cache_key, db_cache.translated_text, 3600)
        return Response({
            'translated_text': db_cache.translated_text,
            'source_language': source_language,
            'target_language': target_language,
            'from_cache': True
        })
    except TranslationCache.DoesNotExist:
        pass

    # 翻訳サービスを使用
    translation_service = TranslationService()
    try:
        translated_text = translation_service.translate(text, source_language, target_language)

        # DBキャッシュに保存
        TranslationCache.objects.update_or_create(
            original_text=text,
            source_language=source_language,
            target_language=target_language,
            defaults={'translated_text': translated_text}
        )

        # メモリキャッシュに保存
        cache.set(cache_key, translated_text, 3600)

        return Response({
            'translated_text': translated_text,
            'source_language': source_language,
            'target_language': target_language,
            'from_cache': False
        })
    except Exception as e:
        return Response({
            'error': str(e),
            'translated_text': text  # エラー時は元のテキストを返す
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def translate_batch(request):
    """複数テキストの一括翻訳"""
    texts = request.data.get('texts', [])
    target_language = request.data.get('target_language', 'en')
    source_language = request.data.get('source_language', 'ja')

    if not texts:
        return Response({'error': 'Texts array is required'}, status=status.HTTP_400_BAD_REQUEST)

    results = []
    translation_service = TranslationService()

    for text in texts:
        # キャッシュチェック
        cache_key = f"translation:{hashlib.md5(f'{text}:{source_language}:{target_language}'.encode()).hexdigest()}"
        cached = cache.get(cache_key)

        if cached:
            results.append({
                'original': text,
                'translated': cached,
                'from_cache': True
            })
        else:
            try:
                translated = translation_service.translate(text, source_language, target_language)
                cache.set(cache_key, translated, 3600)

                # DBキャッシュに保存
                TranslationCache.objects.update_or_create(
                    original_text=text,
                    source_language=source_language,
                    target_language=target_language,
                    defaults={'translated_text': translated}
                )

                results.append({
                    'original': text,
                    'translated': translated,
                    'from_cache': False
                })
            except Exception:
                results.append({
                    'original': text,
                    'translated': text,  # エラー時は元のテキスト
                    'from_cache': False,
                    'error': True
                })

    return Response({
        'translations': results,
        'target_language': target_language
    })

@api_view(['GET', 'PUT'])
@permission_classes([IsAuthenticated])
def language_preference(request):
    """ユーザーの言語設定"""
    if request.method == 'GET':
        try:
            preference = UserLanguagePreference.objects.get(user=request.user)
            return Response({
                'preferred_language': preference.preferred_language,
                'auto_translate': preference.auto_translate
            })
        except UserLanguagePreference.DoesNotExist:
            return Response({
                'preferred_language': 'ja',
                'auto_translate': True
            })

    elif request.method == 'PUT':
        preferred_language = request.data.get('preferred_language', 'ja')
        auto_translate = request.data.get('auto_translate', True)

        preference, created = UserLanguagePreference.objects.update_or_create(
            user=request.user,
            defaults={
                'preferred_language': preferred_language,
                'auto_translate': auto_translate
            }
        )

        return Response({
            'preferred_language': preference.preferred_language,
            'auto_translate': preference.auto_translate,
            'updated': True
        })