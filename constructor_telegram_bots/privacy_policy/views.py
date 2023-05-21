from django.core.handlers.wsgi import WSGIRequest
from django.shortcuts import HttpResponse, render


def privacy_policy(request: WSGIRequest) -> HttpResponse:
	return render(request, 'privacy_policy.html')
