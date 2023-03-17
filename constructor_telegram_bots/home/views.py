from django.core.handlers.wsgi import WSGIRequest
from django.shortcuts import HttpResponse, render

from scripts.decorators import SiteDecorators

@SiteDecorators.get_user_data
def home(request: WSGIRequest, data: dict) -> HttpResponse:
	return render(request, 'home.html', context=data)