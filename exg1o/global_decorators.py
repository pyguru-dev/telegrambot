from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponseBadRequest
from django.shortcuts import redirect
import json

def if_user_authed(func): # Декоратор для проверки авторизован ли пользователь
	def wrapper(*args, **kwargs):
		request: WSGIRequest = args[0]
		if request.user.is_authenticated == True:
			login: str = request.user.username
			nickname: str = kwargs['nickname']
			if nickname == login:
				return func(*args, **kwargs)
			else:
				return HttpResponseBadRequest(f'Ваш Login "{login}", а не "{nickname}"')
		else:
			return redirect('/authorization/')
	wrapper.__name__ = func.__name__
	return wrapper

def check_request_data_items(needs_items: dict): # Декоратор для проверки значений в request запросе
	def decorator(func):
		def wrapper(*args, **kwargs):
			request: WSGIRequest = args[0]
			if request.method == 'POST':
				data = json.loads(request.body)

				data_items = []
				for data_item in tuple(data.items()):
					data_items.append(data_item[0])

				if data_items == needs_items:
					kwargs.update(
						{
							'data': data
						}
					)
					return func(*args, **kwargs)
				else:
					return HttpResponseBadRequest('В тело запроса переданы неправильные данные!')
			else:
				return HttpResponseBadRequest('Неправильный метод запроса!')
		wrapper.__name__ = func.__name__
		return wrapper
	return decorator