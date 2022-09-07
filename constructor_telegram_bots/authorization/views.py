from django.core.handlers.wsgi import WSGIRequest
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseBadRequest, Http404
from django.shortcuts import HttpResponse, render
from django.contrib.auth.models import User
from django.contrib import auth
import global_decorators as GlobalDecorators

# Create your views here.
@GlobalDecorators.if_user_not_authed
@GlobalDecorators.get_navbar_data
def authorization_page(request: WSGIRequest, data: dict): # Отрисовка authorization.html
	return render(request, 'authorization.html', data)

@csrf_exempt
@GlobalDecorators.if_user_not_authed
@GlobalDecorators.check_request_data_items(needs_items=['login', 'password'])
def authorize_in_account(request: WSGIRequest, data: dict): # Авторизация в аккаунт
	login, password = data['login'], data['password']

	if User.objects.filter(username=login).exists():
		user = auth.authenticate(username=login, password=password)
		if user != None:
			auth.login(request, user)

			return HttpResponse('Успешная авторизация.')
		else:
			return HttpResponseBadRequest('Вы ввели неверный "Password"!')
	else:
		return HttpResponseBadRequest('Такого пользователя не существует!')