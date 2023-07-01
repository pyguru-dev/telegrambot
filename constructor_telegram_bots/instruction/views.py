from django.core.handlers.wsgi import WSGIRequest
from django.shortcuts import HttpResponse, render


def instruction(request: WSGIRequest) -> HttpResponse:
	return render(request, 'instruction.html')
