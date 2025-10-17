"""
Template tags and filters for multilanguage translation support
"""
from django import template

register = template.Library()


@register.filter
def get_translation(obj, language_code):
    """
    Get translation for an object based on language code.
    Falls back to Indonesian if translation not found.

    Usage in template:
        {{ text_block|get_translation:user.native_language }}
        {{ vocab|get_translation:'en' }}
    """
    if not obj:
        return ''

    # Try to get from translations JSONField first
    if hasattr(obj, 'translations') and obj.translations:
        translation = obj.translations.get(language_code)
        if translation:
            return translation

    # Fallback to Indonesian field
    if hasattr(obj, 'indonesian_translation'):
        return obj.indonesian_translation
    elif hasattr(obj, 'indonesian_name'):
        return obj.indonesian_name
    elif hasattr(obj, 'explanation_indonesian'):
        return obj.explanation_indonesian

    return ''


@register.filter
def get_subject_name(subject, language_code):
    """
    Get subject name in specified language.
    Falls back to Indonesian name if translation not found.

    Usage:
        {{ subject|get_subject_name:user.native_language }}
    """
    if not subject:
        return ''

    # Try translations first
    if hasattr(subject, 'translations') and subject.translations:
        translation = subject.translations.get(language_code)
        if translation:
            return translation

    # Fallback to Indonesian
    if hasattr(subject, 'indonesian_name') and subject.indonesian_name:
        return subject.indonesian_name

    # Final fallback to name
    return subject.name if hasattr(subject, 'name') else ''


@register.simple_tag
def translate_text(translations_dict, language_code, fallback=''):
    """
    Get translation from a translations dictionary.

    Usage:
        {% translate_text text_block.translations user.native_language text_block.indonesian_translation %}
    """
    if not translations_dict:
        return fallback

    translation = translations_dict.get(language_code)
    if translation:
        return translation

    # Try Indonesian as fallback
    indonesian = translations_dict.get('id')
    if indonesian:
        return indonesian

    return fallback


@register.simple_tag
def get_available_languages(obj):
    """
    Get list of available language codes for an object.

    Usage:
        {% get_available_languages text_block as languages %}
    """
    if not obj or not hasattr(obj, 'translations'):
        return ['id']  # Indonesian only

    available = list(obj.translations.keys()) if obj.translations else []

    # Always include Indonesian
    if 'id' not in available:
        available.append('id')

    return available


@register.inclusion_tag('learning/language_badge.html')
def show_language_badge(obj):
    """
    Display badge showing available languages for an object.

    Usage:
        {% show_language_badge text_block %}
    """
    languages = []
    if obj and hasattr(obj, 'translations') and obj.translations:
        languages = list(obj.translations.keys())

    # Always include Indonesian
    if 'id' not in languages:
        languages.append('id')

    return {'languages': languages}
