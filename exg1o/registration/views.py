from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponseBadRequest, Http404
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import HttpResponse, render
from django.contrib.auth.models import User, Group
import global_methods as GlobalMethods
import json
import os

# Create your views here.
def registration_page(request: WSGIRequest): # Отрисовка registration.html
	if request.user.is_authenticated == False:
		data = GlobalMethods.get_navbar_buttons_data(request)
		return render(request, 'registration.html', data)
	else:
		raise Http404('Сначала выйдите из акканута!')

@csrf_exempt
def register_account(request: WSGIRequest): # Регистрация аккаунта
	if request.user.is_authenticated == False:
		if request.method == 'POST':
			data = json.loads(request.body)
			data_items = tuple(data.items())
			if (data_items[0][0], data_items[1][0], data_items[2][0]) == ('login', 'email', 'password'):
				login, email, password = data['login'], data['email'], data['password']

				if User.objects.filter(username=login).exists() == False:
					user = User.objects.create_user(login, email, password)

					free_accounts_group = Group.objects.get(name='free_accounts')
					user.groups.add(free_accounts_group)

					os.mkdir(f'files/users/{login}')

					user.save()

					return HttpResponse('Успешная регистрация.')
				else:
					return HttpResponseBadRequest(f'Login "{login}" уже занят!')
			else:
				return HttpResponseBadRequest('В тело запроса переданы неправильные данные!')
		else:
			return HttpResponseBadRequest('Неправильный метод запроса!')
	else:
		raise Http404('Сначала выйдите из акканута!')