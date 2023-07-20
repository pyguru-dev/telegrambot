from .models import TeamMember


def team_members(*args, **kwargs) -> dict:
    return {'team_members': TeamMember.objects.all()}
