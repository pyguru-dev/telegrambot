from django.core.handlers.wsgi import WSGIRequest
from django.shortcuts import HttpResponse, render

from team.models import TeamMember


def team(request: WSGIRequest) -> HttpResponse:
	return render(request, 'team.html', {'team_members': TeamMember.objects.all()})
