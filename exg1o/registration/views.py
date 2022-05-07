from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import HttpResponse, render
from django.contrib.auth.models import User
import global_methods as GlobalMethods
import json

# Create your views here.
def registration(request: WSGIRequest): # Отрисовка registration.html
	data = GlobalMethods.get_navbar_buttons_data(request)
	return render(request, 'registration.html', data)

@csrf_exempt
def register_account(request: WSGIRequest): # Регистрация аккаунта
	if request.method == 'POST':
		data = json.loads(request.body)
		data_items = tuple(data.items())
		if (data_items[0][0], data_items[1][0], data_items[2][0]) == ('login', 'email', 'password'):
			login, email, password = data['login'], data['email'], data['password']

			if User.objects.filter(username=login).exists() == False:
				user = User.objects.create_user(login, email, password)
				user.save()

				return HttpResponse('Успешная регистрация.')
			else:
				return HttpResponseBadRequest(f'Login "{login}" уже занят!')
		else:
			return HttpResponseBadRequest('В тело запроса переданы неправильные данные!')
	else:
		return HttpResponseBadRequest('Неправильный метод запроса!')