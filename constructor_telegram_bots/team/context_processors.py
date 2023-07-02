from django.core.handlers.wsgi import WSGIRequest

from team.models import TeamMember


def team_members(request: WSGIRequest) -> dict:
    return {'team_members': TeamMember.objects.all()}
