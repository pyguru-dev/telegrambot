from django.http import HttpRequest, JsonResponse
from django.utils.translation import gettext as _

from rest_framework.request import Request
from rest_framework.response import Response

from constructor_telegram_bots.functions import is_valid_url
from telegram_bot.functions import check_telegram_bot_api_token as check_telegram_bot_api_token_

from telegram_bot.models import TelegramBot, TelegramBotCommand, TelegramBotCommandKeyboard

from functools import wraps
from typing import Union


def check_telegram_bot_api_token(func):
	@wraps(func)
	def wrapper(*args, **kwargs):
		request: Request = args[0]
		api_token: str = kwargs['api_token']

		if not api_token:
			return Response(
				{
					'message': _('Введите API-токен Telegram бота!'),
					'level': 'danger',
				},
				status=400
			)

		if request.user.telegram_bots.filter(api_token=api_token).exists():
			return Response(
				{
					'message': _('Вы уже используете этот API-токен Telegram бота на сайте!'),
					'level': 'danger',
				},
				status=400
			)
		elif TelegramBot.objects.filter(api_token=api_token).exists():
			return Response(
				{
					'message': _('Этот API-токен Telegram бота уже использует другой пользователь сайта!'),
					'level': 'danger',
				},
				status=400
			)

		if not check_telegram_bot_api_token_(api_token):
			return Response(
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
		request: Union[HttpRequest, Request] = args[-1]
		telegram_bot_id: int = kwargs.pop('telegram_bot_id')

		if not request.user.telegram_bots.filter(id=telegram_bot_id).exists():
			data = {
				'message': _('Telegram бот не найден!'),
				'level': 'danger',
			}

			if isinstance(request, HttpRequest):
				return JsonResponse(data, status=400)
			else:
				return Response(data, status=400)

		return func(
			telegram_bot=request.user.telegram_bots.get(id=telegram_bot_id),
			*args,
			**kwargs
		)
	return wrapper

def check_data_for_telegram_bot_command(func):
	@wraps(func)
	def wrapper(*args, **kwargs):
		request: Request = args[0]
		name: str = kwargs['name']
		message_text: str = kwargs['message_text']
		command: Union[str, None] = kwargs['command']
		keyboard: Union[dict, None] = kwargs['keyboard']
		api_request: Union[dict, None] = kwargs['api_request']

		if name:
			if len(name) >= 255:
				return Response(
					{
						'message': _('Название команды должно содержать не более 255 символов!'),
						'level': 'danger',
					},
					status=400
				)
		else:
			return Response(
				{
					'message': _('Введите название команде!'),
					'level': 'danger',
				},
				status=400
			)

		if message_text:
			if len(message_text) >= 4096:
				return Response(
					{
						'message': _('Текст сообщения должно содержать не более 4096 символов!'),
						'level': 'danger',
					},
					status=400
				)
		else:
			return Response(
				{
					'message': _('Введите текст сообщения!'),
					'level': 'danger',
				},
				status=400
			)

		if command is not None:
			if command:
				if len(command) >= 32:
					return Response(
						{
							'message': _('Команда должна содержать не более 32 символов!'),
							'level': 'danger',
						},
						status=400
					)
			else:
				return Response(
					{
						'message': _('Введите команду!'),
						'level': 'danger',
					},
					status=400
				)

		if 'image' in request.FILES:
			kwargs.update({'image': request.FILES['image']})
		elif 'image' in request.POST:
			kwargs.update({'image': request.POST['image']})
		else:
			kwargs.update({'image': None})

		if keyboard is not None:
			for keyboard_button in keyboard['buttons']:
				if ('row' not in keyboard_button or 'text' not in keyboard_button or 'url' not in keyboard_button):
					return Response(
						{
							'message': _('В тело запроса переданы не все данные!'),
							'level': 'danger',
						},
						status=400
					)

				for key, value in keyboard_button.items():
					is_instance = True

					if key == 'row':
						is_instance = isinstance(value, Union[int, None])
					elif key == 'text':
						is_instance = isinstance(value, str)
					elif key == 'url':
						is_instance = isinstance(value, Union[str, None])

					if not is_instance:
						return Response(
							{
								'message': _('В тело запроса передан неверный тип данных!'),
								'level': 'danger',
							},
							status=400
						)

				if (keyboard_button['url'] and not is_valid_url(keyboard_button['url'])):
					return Response(
						{
							'message': _('Введите правильный URL-адрес!'),
							'level': 'danger',
						},
						status=400
					)

		if api_request is not None:
			if ('url' not in api_request or 'data' not in api_request):
				return Response(
					{
						'message': _('В тело запроса переданы не все данные!'),
						'level': 'danger',
					},
					status=400
				)

			for key, value in api_request.items():
				if not isinstance(value, str):
					return Response(
						{
							'message': _('В тело запроса передан неверный тип данных!'),
							'level': 'danger',
						},
						status=400
					)

			if not is_valid_url(api_request['url']):
				return Response(
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
		telegram_bot_command_id: int = kwargs.pop('telegram_bot_command_id')

		if not telegram_bot.commands.filter(id=telegram_bot_command_id).exists():
			return Response(
				{
					'message': _('Команда Telegram бота не найдена!'),
					'level': 'danger',
				},
				status=400
			)

		return func(
			telegram_bot_command=telegram_bot.commands.get(id=telegram_bot_command_id),
			*args,
			**kwargs
		)
	return wrapper

def check_telegram_bot_command_keyboard_button_id(func):
	@wraps(func)
	def wrapper(*args, **kwargs):
		telegram_bot_command: TelegramBotCommand = kwargs['telegram_bot_command']
		telegram_bot_command_keyboard: TelegramBotCommandKeyboard = telegram_bot_command.keyboard
		telegram_bot_command_keyboard_button_id: int = kwargs.pop('telegram_bot_command_keyboard_button_id')

		if not telegram_bot_command_keyboard.buttons.filter(id=telegram_bot_command_keyboard_button_id).exists():
			return Response(
				{
					'message': _('Кнопка клавиатуры команды Telegram бота не найдена!'),
					'level': 'danger',
				},
				status=400
			)

		return func(
			telegram_bot_command_keyboard_button=telegram_bot_command_keyboard.buttons.get(id=telegram_bot_command_keyboard_button_id),
			*args,
			**kwargs
		)
	return wrapper

def check_telegram_bot_user_id(func):
	def wrapper(*args, **kwargs):
		telegram_bot: TelegramBot = kwargs['telegram_bot']
		telegram_bot_user_id: int = kwargs.pop('telegram_bot_user_id')

		if not telegram_bot.users.filter(id=telegram_bot_user_id).exists():
			return Response(
				{
					'message': _('Пользователь Telegram бота не найдена!'),
					'level': 'danger',
				},
				status=400
			)

		return func(
			telegram_bot_user=telegram_bot.users.get(id=telegram_bot_user_id),
			*args,
			**kwargs
		)
	return wrapper
