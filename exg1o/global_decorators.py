from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponseBadRequest
from django.shortcuts import redirect
from konstruktor.models import TelegramBotModel, TelegramBotCommandModel
import json

def if_user_authed(func): # Декоратор для проверки авторизован ли пользователь
	def wrapper(*args, **kwargs):
		request: WSGIRequest = args[0]
		if request.user.is_authenticated == True:
			login, nickname = request.user.username, kwargs['nickname']
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

def check_bot_id(func): # Декоратор для проверки ID бота
	def wrapper(*args, **kwargs):
		nickname, bot_id = kwargs['nickname'], kwargs['bot_id']

		bot = TelegramBotModel.objects.filter(owner=nickname)
		if bot.filter(id=bot_id).exists():
			bot = bot.get(id=bot_id)

			kwargs.update(
				{
					'bot': bot
				}
			)

			return func(*args, **kwargs)
		else:
			return redirect(f'/account/konstruktor/{nickname}/')
	wrapper.__name__ = func.__name__
	return wrapper

def check_command_id(func): # Декоратор для проверки ID команды бота
	def wrapper(*args, **kwargs):
		nickname, bot_id, command_id = kwargs['nickname'],  kwargs['bot_id'], kwargs['command_id']

		bot_command = TelegramBotCommandModel.objects.filter(owner=nickname).filter(bot_id=bot_id)
		if bot_command.filter(id=command_id).exists():
			bot_command = bot_command.get(id=command_id)

			kwargs.update(
				{
					'bot_command': bot_command
				}
			)

			return func(*args, **kwargs)
		else:
			return redirect(f'/account/konstruktor/{nickname}/view_bot/{bot_id}/')
	wrapper.__name__ = func.__name__
	return wrapper
