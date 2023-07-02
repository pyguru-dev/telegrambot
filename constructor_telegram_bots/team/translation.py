from modeltranslation.translator import register, TranslationOptions

from team.models import TeamMember


@register(TeamMember)
class TeamMemberTranslationOptions(TranslationOptions):
    fields = ('speciality',)
