from django.http import HttpRequest, HttpResponse
from django.shortcuts import render


def team(request: HttpRequest) -> HttpResponse:
	return render(request, 'team.html')
