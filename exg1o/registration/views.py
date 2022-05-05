from django.http import HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import HttpResponse, render
from global_variables import lock, sql, db
from global_methods import encrypt
import json

# Create your views here.
def registration(request): # Отрисовка registration.html
	return render(request, 'registration.html')

@csrf_exempt
def register_account(request): # Регистрация аккаунта
	if request.method == 'POST':
		data = json.loads(request.body)
		data_items = tuple(data.items())
		if (data_items[0][0], data_items[1][0], data_items[2][0]) == ('Login', 'Email', 'Password'):
			login, email, password = data['Login'], data['Email'], data['Password']

			sql.execute(f"SELECT * FROM Accounts WHERE Login = '{login}'")
			other_account = sql.fetchone()
			if other_account == None:
				encrypted_password = encrypt(password, password)

				lock.acquire(True)
				sql.execute("INSERT INTO Accounts VALUES (?, ?, ?)", (login, email, encrypted_password))
				db.commit()
				lock.release()

				return HttpResponse('Успешная регистрация.')
			else:
				return HttpResponseBadRequest(f'Login "{login}" уже занят!')
		else:
			return HttpResponseBadRequest('В тело запроса переданы неправильные данные!')
	else:
		return HttpResponseBadRequest('Неправильный метод запроса!')