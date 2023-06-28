from modeltranslation.translator import register, TranslationOptions

from team.models import TeamMembers


@register(TeamMembers)
class TeamMembersTranslationOptions(TranslationOptions):
    fields = ('speciality',)
