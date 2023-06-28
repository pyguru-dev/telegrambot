from modeltranslation.translator import register, TranslationOptions

from updates.models import Updates


@register(Updates)
class UpdatesTranslationOptions(TranslationOptions):
    fields = ('title', 'description')
