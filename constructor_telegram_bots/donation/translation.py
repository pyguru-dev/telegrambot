from modeltranslation.translator import register, TranslationOptions

from .models import DonationSection


@register(DonationSection)
class DonationSectionTranslationOptions(TranslationOptions):
    fields = ('title', 'text')
