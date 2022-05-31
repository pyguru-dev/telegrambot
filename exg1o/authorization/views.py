from django.core.handlers.wsgi import WSGIRequest
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseBadRequest, Http404
from django.shortcuts import HttpResponse, render
from django.contrib.auth.models import User
from django.contrib import auth
import global_functions as GlobalFunctions
import json

# Create your views here.
def authorization_page(request: WSGIRequest): # Отрисовка authorization.html
	if request.user.is_authenticated == False:
		data = GlobalFunctions.get_navbar_buttons_data(request)
		return render(request, 'authorization.html', data)
	else:
		raise Http404('Вы уже авторизованы!')

@csrf_exempt
def authorize_in_account(request: WSGIRequest): # Авторизация в аккаунт
	if request.user.is_authenticated == False:
		if request.method == 'POST':
			data = json.loads(request.body)
			data_items = tuple(data.items())
			if (data_items[0][0], data_items[1][0]) == ('login', 'password'):
				login, password = data['login'], data['password']

				if User.objects.filter(username=login).exists():
					user = auth.authenticate(username=login, password=password)
					if user != None:
						auth.login(request, user)

						return HttpResponse('Успешная авторизация.')
					else:
						return HttpResponseBadRequest('Вы ввели неверный "Password"!')
				else:
					return HttpResponseBadRequest(f'Пользователя "{login}\" не существует!')
			else:
				return HttpResponseBadRequest('В тело запроса переданы неправильные данные!')
		else:
			return HttpResponseBadRequest('Неправильный метод запроса!')
	else:
		raise Http404('Вы уже авторизованы!')