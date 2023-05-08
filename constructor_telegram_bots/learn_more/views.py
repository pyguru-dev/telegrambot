from django.core.handlers.wsgi import WSGIRequest
from django.shortcuts import HttpResponse, render


def learn_more(request: WSGIRequest) -> HttpResponse:
	return render(request=request, template_name='learn_more.html')
