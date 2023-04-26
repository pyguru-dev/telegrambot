from django.core.handlers.wsgi import WSGIRequest
from django.shortcuts import HttpResponse, render

def home(request: WSGIRequest) -> HttpResponse:
	return render(request=request, template_name='home.html')
