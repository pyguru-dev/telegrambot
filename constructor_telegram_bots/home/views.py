from django.core.handlers.wsgi import WSGIRequest
from django.shortcuts import render

# Create your views here.
def home(request: WSGIRequest): # Отрисовка home.html
	return render(request, 'home.html')