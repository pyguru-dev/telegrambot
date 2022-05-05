from django.http import HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import HttpResponse, render
from global_variables import sql
from global_methods import encrypt
import json

# Create your views here.
def authorization(request): # Отрисовка authorization.html
	return render(request, 'authorization.html')

@csrf_exempt
def authorize_in_account(request): # Авторизация в аккаунт
	if request.method == 'POST':
		data = json.loads(request.body)
		data_items = tuple(data.items())
		if (data_items[0][0], data_items[1][0]) == ('Login', 'Password'):
			login, password = data['Login'], data['Password']

			sql.execute(f"SELECT * FROM Accounts WHERE Login = '{login}'")
			account = sql.fetchone()
			if account != None:
				encrypted_password = encrypt(password, password)

				if encrypted_password == account[2]:
					return HttpResponse('Успешная авторизация.')
				else:
					return HttpResponseBadRequest('Вы ввели неверный "Password"!')
			else:
				return HttpResponseBadRequest(f"Пользователя \"{data['Login']}\" не существует!")
		else:
			return HttpResponseBadRequest('В тело запроса переданы неправильные данные!')
	else:
		return HttpResponseBadRequest('Неправильный метод запроса!')