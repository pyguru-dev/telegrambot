from django.core.handlers.wsgi import WSGIRequest
from django.shortcuts import render

import scripts.decorators as Decorators

# Create your views here.
@Decorators.get_user_data
def home(request: WSGIRequest, data: dict):
	return render(request, 'home.html', context=data)