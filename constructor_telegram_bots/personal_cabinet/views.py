from django.core.handlers.wsgi import WSGIRequest
from django.shortcuts import render

import scripts.decorators as Decorators

# Create your views here.
@Decorators.get_user_data
def personal_cabinet(request: WSGIRequest, data: dict):
	return render(request, 'personal_cabinet.html', context=data)