from django.http import HttpRequest

from team.models import TeamMember


def team_members(request: HttpRequest) -> dict:
    return {'team_members': TeamMember.objects.all()}
