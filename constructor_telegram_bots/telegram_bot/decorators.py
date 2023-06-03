from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponseBadRequest

from django.utils.datastructures import MultiValueDictKeyError

from telegram_bot.models import TelegramBot, TelegramBotCommand, TelegramBotCommandKeyboard
from telegram_bot.functions import check_telegram_bot_api_token as _check_telegram_bot_api_token

from functools import wraps


def check_telegram_bot_api_token(func):
	@wraps(func)
	def wrapper(*args, **kwargs):
		api_token: str = kwargs['api_token']

		if api_token != '':
			request: WSGIRequest = args[0]

			if request.user.telegram_bots.filter(api_token=api_token).exists():
				return HttpResponseBadRequest('Вы уже используете этот API-токен Telegram бота на сайте!')
			elif TelegramBot.objects.filter(api_token=api_token).exists():
				return HttpResponseBadRequest('Этот API-токен Telegram бота уже использует другой пользователь сайта!')

			if _check_telegram_bot_api_token(api_token=api_token) is not None:
				return func(*args, **kwargs)
			else:
				return HttpResponseBadRequest('Ваш API-токен Telegram бота является недействительным!')
		else:
			return HttpResponseBadRequest('Введите API-токен Telegram бота!')
	return wrapper

def check_telegram_bot_id(func):
	@wraps(func)
	def wrapper(*args, **kwargs):
		request: WSGIRequest = args[0]
		telegram_bot_id: int = kwargs['telegram_bot_id']
		
		if request.user.telegram_bots.filter(id=telegram_bot_id).exists():
			del kwargs['telegram_bot_id']
			kwargs.update({'telegram_bot': request.user.telegram_bots.get(id=telegram_bot_id)})

			return func(*args, **kwargs)
		else:
			return HttpResponseBadRequest('Telegram бот не найден!')
	return wrapper

def check_data_for_telegram_bot_command(func):
	@wraps(func)
	def wrapper(*args, **kwargs):
		telegram_bot_command_name: str = kwargs['name']

		if telegram_bot_command_name != '':
			if len(telegram_bot_command_name) <= 255:
				telegram_bot_command_message_text: str = kwargs['message_text']

				if telegram_bot_command_message_text != '':
					if len(telegram_bot_command_message_text) <= 4096:
						telegram_bot_command_command: str = kwargs['command']

						if telegram_bot_command_command is not None:
							if telegram_bot_command_command != '':
								if len(telegram_bot_command_command) >= 32:
									return HttpResponseBadRequest('Команда должна содержать не более 32 символов!')
							else:
								return HttpResponseBadRequest('Введите команду!')
						
						request: WSGIRequest = args[0]

						try:
							if 'image' in request.FILES:
								kwargs.update({'image': request.FILES['image']})
							else:
								if request.POST['image'] == 'null':
									kwargs.update({'image': None})
								else:
									kwargs.update({'image': request.POST['image']})
						except MultiValueDictKeyError:
							kwargs.update({'image': None})

						return func(*args, **kwargs)
					else:
						return HttpResponseBadRequest('Текст сообщения должно содержать не более 4096 символов!')
				else:
					return HttpResponseBadRequest('Введите текст сообщения!')
			else:
				return HttpResponseBadRequest('Название команды должно содержать не более 255 символов!')
		else:
			return HttpResponseBadRequest('Введите название команде!')
	return wrapper

def check_telegram_bot_command_id(func):
	@wraps(func)
	def wrapper(*args, **kwargs):
		telegram_bot: TelegramBot = kwargs['telegram_bot']
		telegram_bot_command_id: int = kwargs['telegram_bot_command_id']

		if telegram_bot.commands.filter(id=telegram_bot_command_id).exists():
			del kwargs['telegram_bot_command_id']
			kwargs.update({'telegram_bot_command': telegram_bot.commands.get(id=telegram_bot_command_id)})

			return func(*args, **kwargs)
		else:
			return HttpResponseBadRequest('Команда Telegram бота не найдена!')
	return wrapper

def check_telegram_bot_command_keyboard_button_id(func):
	@wraps(func)
	def wrapper(*args, **kwargs):
		telegram_bot_command: TelegramBotCommand = kwargs['telegram_bot_command']
		telegram_bot_command_keyboard: TelegramBotCommandKeyboard = telegram_bot_command.keyboard
		telegram_bot_command_keyboard_button_id: int = kwargs['telegram_bot_command_keyboard_button_id']

		if telegram_bot_command_keyboard.buttons.filter(id=telegram_bot_command_keyboard_button_id).exists():
			del kwargs['telegram_bot_command_keyboard_button_id']
			kwargs.update({'telegram_bot_command_keyboard_button': telegram_bot_command_keyboard.buttons.get(id=telegram_bot_command_keyboard_button_id)})

			return func(*args, **kwargs)
		else:
			return HttpResponseBadRequest('Кнопка клавиатуры команды Telegram бота не найдена!')
	return wrapper

def check_telegram_bot_user_id(func):
	def wrapper(*args, **kwargs):
		telegram_bot: TelegramBot = kwargs['telegram_bot']
		telegram_bot_user_id: int = kwargs['telegram_bot_user_id']

		if telegram_bot.users.filter(id=telegram_bot_user_id).exists():
			del kwargs['telegram_bot_user_id']
			kwargs.update({'telegram_bot_user': telegram_bot.users.get(id=telegram_bot_user_id)})

			return func(*args, **kwargs)
		else:
			return HttpResponseBadRequest('Пользователь Telegram бота не найдена!')
	return wrapper
