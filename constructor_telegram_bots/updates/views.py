from django.core.handlers.wsgi import WSGIRequest
from django.shortcuts import HttpResponse, render


def updates(request: WSGIRequest) -> HttpResponse:
	return render(request, 'updates.html')
