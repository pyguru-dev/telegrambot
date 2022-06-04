from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponseBadRequest
from django.shortcuts import redirect

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