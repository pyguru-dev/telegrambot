from django.http import HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import HttpResponse, render
import sqlite3
import json

# Create your views here.
def registration(request): # Отрисовка registration.html
	return render(request, 'registration.html')

@csrf_exempt
def register_account(request): # Регистрация
	if request.method == 'POST':
		data = json.loads(request.body)
		data_items = tuple(data.items())
		if (data_items[0][0], data_items[1][0], data_items[2][0]) == ('Login', 'Email', 'Password'):
			db = sqlite3.connect('../DataBase.db')
			sql = db.cursor()

			sql.execute(f"SELECT * FROM Accounts WHERE Login = \'{data['Login']}\'")
			other_account = sql.fetchone()
			if other_account == None:
				sql.execute("INSERT INTO Accounts VALUES (?, ?, ?)", (data['Login'], data['Email'], data['Password']))
				db.commit()

				return HttpResponse('Успешная регистрация.')
			else:
				return HttpResponseBadRequest(f"Login \"{data['Login']}\" уже занят!")
		else:
			return HttpResponseBadRequest('В тело запроса переданы неправильные данные!')
	else:
		return HttpResponseBadRequest('Неправильный метод запроса!')