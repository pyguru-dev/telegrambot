from django.core.handlers.wsgi import WSGIRequest
from django.http import JsonResponse

from django.utils.translation import gettext as _

from telegram_bot.models import TelegramBot, TelegramBotCommand, TelegramBotCommandKeyboard

from constructor_telegram_bots.functions import is_valid_url
from telegram_bot.functions import check_telegram_bot_api_token as check_telegram_bot_api_token_

from functools import wraps
from typing import Union


def check_telegram_bot_api_token(func):
	@wraps(func)
	def wrapper(*args, **kwargs):
		api_token: str = kwargs['api_token']

		if api_token == '':
			return JsonResponse(
				{
					'message': _('Введите API-токен Telegram бота!'),
					'level': 'danger',
				},
				status=400
			)
		
		request: WSGIRequest = args[0]

		if request.user.telegram_bots.filter(api_token=api_token).exists():
			return JsonResponse(
				{
					'message': _('Вы уже используете этот API-токен Telegram бота на сайте!'),
					'level': 'danger',
				},
				status=400
			)
		elif TelegramBot.objects.filter(api_token=api_token).exists():
			return JsonResponse(
				{
					'message': _('Этот API-токен Telegram бота уже использует другой пользователь сайта!'),
					'level': 'danger',
				},
				status=400
			)

		if check_telegram_bot_api_token_(api_token=api_token) is None:
			return JsonResponse(
				{
					'message': _('Ваш API-токен Telegram бота является недействительным!'),
					'level': 'danger',
				},
				status=400
			)
		
		return func(*args, **kwargs)
	return wrapper

def check_telegram_bot_id(func):
	@wraps(func)
	def wrapper(*args, **kwargs):
		request: WSGIRequest = args[0]
		telegram_bot_id: int = kwargs['telegram_bot_id']

		if request.user.telegram_bots.filter(id=telegram_bot_id).exists() is False:
			return JsonResponse(
				{
					'message': _('Telegram бот не найден!'),
					'level': 'danger',
				},
				status=400
			)

		del kwargs['telegram_bot_id']
		kwargs.update({'telegram_bot': request.user.telegram_bots.get(id=telegram_bot_id)})

		return func(*args, **kwargs)
	return wrapper

def check_data_for_telegram_bot_command(func):
	@wraps(func)
	def wrapper(*args, **kwargs):
		telegram_bot_command_name: str = kwargs['name']

		if telegram_bot_command_name != '':
			if len(telegram_bot_command_name) >= 255:
				return JsonResponse(
					{
						'message': _('Название команды должно содержать не более 255 символов!'),
						'level': 'danger',
					},
					status=400
				)
		else:
			return JsonResponse(
				{
					'message': _('Введите название команде!'),
					'level': 'danger',
				},
				status=400
			)

		telegram_bot_command_command: Union[str, None] = kwargs['command']

		if telegram_bot_command_command is not None:
			if telegram_bot_command_command != '':
				if len(telegram_bot_command_command) >= 32:
					return JsonResponse(
						{
							'message': _('Команда должна содержать не более 32 символов!'),
							'level': 'danger',
						},
						status=400
					)
			else:
				return JsonResponse(
					{
						'message': _('Введите команду!'),
						'level': 'danger',
					},
					status=400
				)

		request: WSGIRequest = args[0]

		if 'image' in request.FILES:
			kwargs.update(
				{
					'image': request.FILES['image'],
				}
			)
		elif 'image' in request.POST:
			kwargs.update(
				{
					'image': request.POST['image'],
				}
			)
		else:
			kwargs.update(
				{
					'image': None,
				}
			)

		telegram_bot_command_message_text: str = kwargs['message_text']

		if telegram_bot_command_message_text != '':
			if len(telegram_bot_command_message_text) >= 4096:
				return JsonResponse(
					{
						'message': _('Текст сообщения должно содержать не более 4096 символов!'),
						'level': 'danger',
					},
					status=400
				)
		else:
			return JsonResponse(
				{
					'message': _('Введите текст сообщения!'),
					'level': 'danger',
				},
				status=400
			)

		telegram_bot_command_keyboard: Union[dict, None] = kwargs['keyboard']

		if telegram_bot_command_keyboard is not None:
			for telegram_bot_command_keyboard_button in telegram_bot_command_keyboard['buttons']:
				if (
					'row' not in telegram_bot_command_keyboard_button or
					'text' not in telegram_bot_command_keyboard_button or
					'url' not in telegram_bot_command_keyboard_button
				):
					return JsonResponse(
						{
							'message': _('В тело запроса переданы не все данные!'),
							'level': 'danger',
						},
						status=400
					)
				
				for key, value in telegram_bot_command_keyboard_button.items():
					if key in ['text', 'url']:
						if isinstance(value, str) is False:
							return JsonResponse(
								{
									'message': _('В тело запроса передан неверный тип данных!'),
									'level': 'danger',
								},
								status=400
							)
					elif key in ['row']:
						if isinstance(value, Union[int, None]) is False:
							return JsonResponse(
								{
									'message': _('В тело запроса передан неверный тип данных!'),
									'level': 'danger',
								},
								status=400
							)
				
				if is_valid_url(telegram_bot_command_keyboard_button['url']) is False:
					return JsonResponse(
						{
							'message': _('Введите правильный URL-адрес!'),
							'level': 'danger',
						},
						status=400
					)

		telegram_bot_command_api_request: Union[dict, None] = kwargs['api_request']

		if telegram_bot_command_api_request is not None:
			if 'url' not in telegram_bot_command_api_request or 'data' not in telegram_bot_command_api_request:
				return JsonResponse(
					{
						'message': _('В тело запроса переданы не все данные!'),
						'level': 'danger',
					},
					status=400
				)
			
			for key, value in telegram_bot_command_api_request.items():
				if isinstance(value, str) is False:
					return JsonResponse(
						{
							'message': _('В тело запроса передан неверный тип данных!'),
							'level': 'danger',
						},
						status=400
					)

			if is_valid_url(telegram_bot_command_api_request['url']) is False:
				return JsonResponse(
					{
						'message': _('Введите правильный URL-адрес!'),
						'level': 'danger',
					},
					status=400
				)

		return func(*args, **kwargs)
	return wrapper

def check_telegram_bot_command_id(func):
	@wraps(func)
	def wrapper(*args, **kwargs):
		telegram_bot: TelegramBot = kwargs['telegram_bot']
		telegram_bot_command_id: int = kwargs['telegram_bot_command_id']

		if telegram_bot.commands.filter(id=telegram_bot_command_id).exists() is False:
			return JsonResponse(
				{
					'message': _('Команда Telegram бота не найдена!'),
					'level': 'danger',
				},
				status=400
			)
		
		del kwargs['telegram_bot_command_id']
		kwargs.update({'telegram_bot_command': telegram_bot.commands.get(id=telegram_bot_command_id)})

		return func(*args, **kwargs)
	return wrapper

def check_telegram_bot_command_keyboard_button_id(func):
	@wraps(func)
	def wrapper(*args, **kwargs):
		telegram_bot_command: TelegramBotCommand = kwargs['telegram_bot_command']
		telegram_bot_command_keyboard: TelegramBotCommandKeyboard = telegram_bot_command.keyboard
		telegram_bot_command_keyboard_button_id: int = kwargs['telegram_bot_command_keyboard_button_id']

		if telegram_bot_command_keyboard.buttons.filter(id=telegram_bot_command_keyboard_button_id).exists() is False:
			return JsonResponse(
				{
					'message': _('Кнопка клавиатуры команды Telegram бота не найдена!'),
					'level': 'danger',
				},
				status=400
			)
		
		del kwargs['telegram_bot_command_keyboard_button_id']
		kwargs.update({'telegram_bot_command_keyboard_button': telegram_bot_command_keyboard.buttons.get(id=telegram_bot_command_keyboard_button_id)})

		return func(*args, **kwargs)
	return wrapper

def check_telegram_bot_user_id(func):
	def wrapper(*args, **kwargs):
		telegram_bot: TelegramBot = kwargs['telegram_bot']
		telegram_bot_user_id: int = kwargs['telegram_bot_user_id']

		if telegram_bot.users.filter(id=telegram_bot_user_id).exists() is False:
			return JsonResponse(
				{
					'message': _('Пользователь Telegram бота не найдена!'),
					'level': 'danger',
				},
				status=400
			)
		
		del kwargs['telegram_bot_user_id']
		kwargs.update({'telegram_bot_user': telegram_bot.users.get(id=telegram_bot_user_id)})

		return func(*args, **kwargs)
	return wrapper
