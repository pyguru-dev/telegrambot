from django.core.handlers.wsgi import WSGIRequest
from django.shortcuts import render
import global_functions as GlobalFunctions

# Create your views here.
def main(request: WSGIRequest): # Отрисовка main.html
	data = GlobalFunctions.get_navbar_buttons_data(request)
	return render(request, 'main.html', data)