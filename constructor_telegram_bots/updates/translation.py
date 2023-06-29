from modeltranslation.translator import register, TranslationOptions

from updates.models import Update


@register(Update)
class UpdateTranslationOptions(TranslationOptions):
    fields = ('title', 'description')
