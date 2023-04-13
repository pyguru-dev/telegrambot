from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponseBadRequest
from django.shortcuts import render

from telegram.update import Update

from telegram_bot.models import TelegramBot, TelegramBotUser

import json

class TelegramBotDecorators:
	def get_attributes(need_attributes: tuple):
		def decorator(func):
			def wrapper(*args, **kwargs):
				update: Update = args[1]

				attributes = {
					'update': update,
					'context': args[2],
					'chat_id': update.effective_chat.id,
					'user_id': update.effective_user.id,
					'username': update.effective_user.username,
				}

				if update.effective_message is not None:
					attributes.update(
						{
							'message': update.effective_message.text,
						}
					)

				if update.callback_query is not None:
					attributes.update(
						{
							'callback_data': update.callback_query.data,
						}
					)

				kwargs = {}
				for attribute in attributes:
					for need_attribute in need_attributes:
						if attribute == need_attribute:
							kwargs.update(
								{
									attribute: attributes[attribute],
								}
							)

				if tuple(kwargs.keys()) == need_attributes:
					kwargs.update(
						{
							'self': args[0],
						}
					)

					return func(**kwargs)
				else:
					return Exception('Func attributes != need attributes!')
			return wrapper
		return decorator
	
	def check_telegram_bot_user(func):
		def wrapper(*args, **kwargs):
			self = kwargs['self']
			update: Update = kwargs['update']

			telegram_bot: TelegramBot = TelegramBot.objects.get(id=self.telegram_bot.id)
			user_id: int = update.effective_user.id

			if telegram_bot.users.filter(user_id=user_id).exists() is False:
				telegram_bot_user: TelegramBotUser = TelegramBotUser(user_id=user_id, username=update.effective_user.username)
				telegram_bot_user.save()

				telegram_bot.users.add(telegram_bot_user)
				telegram_bot.save()

			if telegram_bot.private:
				if telegram_bot.allowed_users.filter(user_id=user_id).exists():
					return func(*args, **kwargs)
			else:
				return func(*args, **kwargs)
		return wrapper
	
#############################################################################################################################

class SiteDecorators:
	def get_user_data(func):
		def wrapper(*args, **kwargs):
			request: WSGIRequest = args[0]

			kwargs.update(
				{
					'data': {
						'page': {
							'url': request.path,
						},
						'user': {
							'is_authenticated': request.user.is_authenticated,
						},
					},
				}
			)

			return func(*args, **kwargs)
		return wrapper

	def is_auth(render_page: bool):
		def decorator(func):
			def wrapper(*args, **kwargs):
				request: WSGIRequest = args[0]

				if request.user.is_authenticated:
					return func(*args, **kwargs)
				else:
					return render(request=request, template_name='404.html', status=404) if render_page else HttpResponseBadRequest('Сначала авторизуйтесь на сайте!')
			return wrapper
		return decorator

	def check_request_data_items(needs_items: tuple):
		def decorator(func):
			def wrapper(*args, **kwargs):
				request: WSGIRequest = args[0]
				
				if request.method == 'POST':
					data: dict = json.loads(request.body)
					data_items: tuple = tuple([data_item for data_item in tuple(data.keys()) if data_item in needs_items])

					if data_items == needs_items:
						for data_item in data_items:
							kwargs.update(
								{
									data_item: data[data_item],
								}
							)

						return func(*args, **kwargs)
					else:
						return HttpResponseBadRequest('В тело запроса переданы не все данные данные!')
				else:
					return HttpResponseBadRequest('Неправильный метод запроса!')
			return wrapper
		return decorator
	
	def check_telegram_bot_token(func):
		def wrapper(*args, **kwargs):
			token: str = kwargs['token']

			if len(token) > 0:
				request: WSGIRequest = args[0]

				if request.user.telegram_bots.filter(token=token).exists():
					return HttpResponseBadRequest('Вы уже используете этот токен Telegram бота на сайте!')
				elif TelegramBot.objects.filter(token=token).exists():
					return HttpResponseBadRequest('Ваш токен Telegram бота уже использует другой пользователь сайта!')

				return func(*args, **kwargs) if TelegramBot.objects.test_telegram_bot_token(token=token) is not None else HttpResponseBadRequest('Ваш токен Telegram бота является недействительным!')
			else:
				return HttpResponseBadRequest('Введите токен Telegram бота!')
				
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
					raise ValueError('The argument telegram_bot_id is missing!')
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
				raise ValueError('The argument telegram_bot_command_id is missing!')
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
				raise ValueError('The argument telegram_bot_user_id is missing!')
		return wrapper
