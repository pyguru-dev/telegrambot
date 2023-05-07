from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponseBadRequest
from django.shortcuts import render

from telegram_bot.models import TelegramBot

import scripts.functions as Functions

import json


def check_post_request_data_items(request_need_items: tuple):
	def decorator(func):
		def wrapper(*args, **kwargs):
			request: WSGIRequest = args[0]
			
			if request.method == 'POST':
				request_data: dict = json.loads(request.body)
				request_data_items: tuple = tuple([request_data_item for request_data_item in tuple(request_data.keys()) if request_data_item in request_need_items])

				if request_data_items == request_need_items:
					for request_data_item in request_data_items:
						kwargs.update(
							{
								request_data_item: request_data[request_data_item],
							}
						)

					return func(*args, **kwargs)
				else:
					return HttpResponseBadRequest('В тело запроса переданы не все данные данные!')
			else:
				return HttpResponseBadRequest('Неправильный метод запроса!')
		return wrapper
	return decorator

def check_telegram_bot_api_token(func):
	def wrapper(*args, **kwargs):
		api_token: str = kwargs['api_token']

		if len(api_token) > 0:
			request: WSGIRequest = args[0]

			if request.user.telegram_bots.filter(api_token=api_token).exists():
				return HttpResponseBadRequest('Вы уже используете этот API-токен Telegram бота на сайте!')
			elif TelegramBot.objects.filter(api_token=api_token).exists():
				return HttpResponseBadRequest('Этот API-токен Telegram бота уже использует другой пользователь сайта!')

			return func(*args, **kwargs) if Functions.check_telegram_bot_api_token(api_token=api_token) is not None else HttpResponseBadRequest('Ваш API-токен Telegram бота является недействительным!')
		else:
			return HttpResponseBadRequest('Введите API-токен Telegram бота!')
			
	return wrapper

def check_telegram_bot_id(render_page: bool):
	def decorator(func):
		def wrapper(*args, **kwargs):
			if 'telegram_bot_id' in kwargs:
				request: WSGIRequest = args[0]
				telegram_bot_id: int = kwargs['telegram_bot_id']

				if request.user.telegram_bots.filter(id=telegram_bot_id).exists():
					del kwargs['telegram_bot_id']

					kwargs.update(
						{
							'telegram_bot': request.user.telegram_bots.get(id=telegram_bot_id),
						}
					)

					return func(*args, **kwargs)
				else:
					return render(request=request, template_name='404.html', status=404) if render_page else HttpResponseBadRequest('Telegram бот не найден!')
			else:
				raise ValueError('Argument "telegram_bot_id" is missing!')
		return wrapper
	return decorator

def check_data_for_telegram_bot_command(func):
	def wrapper(*args, **kwargs):
		name: str = kwargs['name']

		if name != '':
			if len(name) <= 255:
				command: str = kwargs['command']
				callback: str = kwargs['callback']

				if command == '' and callback == '':
					return HttpResponseBadRequest('Придумайте команду или введите CallBack текст!')
				else:
					if len(command) >= 32:
						return HttpResponseBadRequest('Команда должна содержать не более 32 символов!')

					if len(callback) >= 64:
						return HttpResponseBadRequest('CallBack текст должен содержать не более 64 символов!')
					
					return func(*args, **kwargs) if kwargs['message_text'] != '' else HttpResponseBadRequest('Введите текст сообщения!')
			else:
				return HttpResponseBadRequest('Название команды должно содержать не более 255 символов!')
		else:
			return HttpResponseBadRequest('Придумайте название команде!')
	return wrapper

def check_telegram_bot_command_id(func):
	def wrapper(*args, **kwargs):
		if 'telegram_bot_command_id' in kwargs:
			telegram_bot: TelegramBot = kwargs['telegram_bot']
			telegram_bot_command_id: int = kwargs['telegram_bot_command_id']

			if telegram_bot.commands.filter(id=telegram_bot_command_id).exists():
				del kwargs['telegram_bot_command_id']

				kwargs.update(
					{
						'telegram_bot_command': telegram_bot.commands.get(id=telegram_bot_command_id),
					}
				)

				return func(*args, **kwargs)
			else:
				return HttpResponseBadRequest('Команда Telegram бота не найдена!')
		else:
			raise ValueError('Argument "telegram_bot_command_id" is missing!')
	return wrapper

def check_telegram_bot_user_id(func):
	def wrapper(*args, **kwargs):
		if 'telegram_bot_user_id' in kwargs:
			telegram_bot: TelegramBot = kwargs['telegram_bot']
			telegram_bot_user_id: int = kwargs['telegram_bot_user_id']

			if telegram_bot.users.filter(id=telegram_bot_user_id).exists():
				del kwargs['telegram_bot_user_id']

				kwargs.update(
					{
						'telegram_bot_user': telegram_bot.users.get(id=telegram_bot_user_id),
					}
				)

				return func(*args, **kwargs)
			else:
				return HttpResponseBadRequest('Пользователь Telegram бота не найдена!')
		else:
			raise ValueError('Argument "telegram_bot_user_id" is missing!')
	return wrapper
