from django.core.handlers.wsgi import WSGIRequest
from django.shortcuts import HttpResponse, render

def privacy_policy(request: WSGIRequest) -> HttpResponse:
	return render(request=request, template_name='privacy_policy.html')
