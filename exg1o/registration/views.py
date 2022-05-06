from django.http import HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import HttpResponse, render
from django.contrib.auth.models import User
import json

# Create your views here.
def registration(request): # Отрисовка registration.html
	return render(request, 'registration.html')

@csrf_exempt
def register_account(request): # Регистрация аккаунта
	if request.method == 'POST':
		data = json.loads(request.body)
		data_items = tuple(data.items())
		if (data_items[0][0], data_items[1][0], data_items[2][0]) == ('login', 'email', 'password'):
			login, email, password = data['login'], data['email'], data['password']

			try:
				User.objects.get(username=login)

				return HttpResponseBadRequest(f'Login "{login}" уже занят!')
			except User.DoesNotExist:
				user = User.objects.create_user(login, email, password)
				user.save()

				return HttpResponse('Успешная регистрация.')
		else:
			return HttpResponseBadRequest('В тело запроса переданы неправильные данные!')
	else:
		return HttpResponseBadRequest('Неправильный метод запроса!')