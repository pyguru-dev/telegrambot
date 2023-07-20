from modeltranslation.translator import register, TranslationOptions

from .models import Update


@register(Update)
class UpdateTranslationOptions(TranslationOptions):
    fields = ('description',)
