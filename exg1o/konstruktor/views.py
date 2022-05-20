from django.core.handlers.wsgi import WSGIRequest
from django.http import Http404
from django.shortcuts import render
import global_methods as GlobalMethods

# Create your views here.
def konstruktor(request: WSGIRequest, nickname: str): # Отрисовка konstruktor.html
	if request.user.is_authenticated:
		data = GlobalMethods.get_navbar_buttons_data(request)
		return render(request, 'konstruktor.html', data)
	else:
		raise Http404('Сначала войдите в акканут!')

def add_bot(request: WSGIRequest, nickname: str): # Отрисовка add_bot.html
	if request.user.is_authenticated:
		data = GlobalMethods.get_navbar_buttons_data(request)
		return render(request, 'add_bot.html', data)
	else:
		raise Http404('Сначала войдите в акканут!')
