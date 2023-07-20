from modeltranslation.translator import register, TranslationOptions

from .models import TeamMember


@register(TeamMember)
class TeamMemberTranslationOptions(TranslationOptions):
    fields = ('speciality',)
