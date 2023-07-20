from django.http import HttpRequest, HttpResponse
from django.shortcuts import render


def team_view(request: HttpRequest) -> HttpResponse:
	return render(request, 'team.html')
