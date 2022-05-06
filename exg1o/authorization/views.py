from django.http import HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import HttpResponse, render
from django.contrib.auth.models import User
from django.contrib import auth
import json

# Create your views here.
def authorization(request): # Отрисовка authorization.html
	return render(request, 'authorization.html')

@csrf_exempt
def authorize_in_account(request): # Авторизация в аккаунт
	if request.method == 'POST':
		data = json.loads(request.body)
		data_items = tuple(data.items())
		if (data_items[0][0], data_items[1][0]) == ('login', 'password'):
			login, password = data['login'], data['password']

			try:
				User.objects.get(username=login)
				user = auth.authenticate(username=login, password=password)
				if user != None:
					return HttpResponse('Успешная авторизация.')
				else:
					return HttpResponseBadRequest('Вы ввели неверный "Password"!')
			except User.DoesNotExist:
				return HttpResponseBadRequest(f"Пользователя \"{data['Login']}\" не существует!")
		else:
			return HttpResponseBadRequest('В тело запроса переданы неправильные данные!')
	else:
		return HttpResponseBadRequest('Неправильный метод запроса!')