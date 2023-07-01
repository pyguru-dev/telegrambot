from modeltranslation.translator import register, TranslationOptions

from instruction.models import InstructionSection


@register(InstructionSection)
class InstructionSectionTranslationOptions(TranslationOptions):
    fields = ('title', 'text')
