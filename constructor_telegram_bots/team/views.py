from django.core.handlers.wsgi import WSGIRequest
from django.shortcuts import HttpResponse, render


def team(request: WSGIRequest) -> HttpResponse:
	return render(request, 'team.html')
