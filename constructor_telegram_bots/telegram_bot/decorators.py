from django.http import HttpRequest, JsonResponse
from django.utils.translation import gettext as _

from rest_framework.request import Request
from rest_framework.response import Response

from .models import TelegramBot, TelegramBotCommand, TelegramBotCommandKeyboard

from functools import wraps
from typing import Union


def check_telegram_bot_id(func):
	@wraps(func)
	def wrapper(*args, **kwargs):
		request: Union[HttpRequest, Request] = args[-1]
		telegram_bot_id: int = kwargs.pop('telegram_bot_id')

		if not request.user.telegram_bots.filter(id=telegram_bot_id).exists():
			return (JsonResponse if isinstance(request, HttpRequest) else Response)({
				'message': _('Telegram бот не найден!'),
				'level': 'danger',
			}, status=404)

		return func(telegram_bot=request.user.telegram_bots.get(id=telegram_bot_id), *args, **kwargs)
	return wrapper

def check_telegram_bot_command_id(func):
	@wraps(func)
	def wrapper(*args, **kwargs):
		telegram_bot: TelegramBot = kwargs['telegram_bot']
		telegram_bot_command_id: int = kwargs.pop('telegram_bot_command_id')

		if not telegram_bot.commands.filter(id=telegram_bot_command_id).exists():
			return Response({
				'message': _('Команда Telegram бота не найдена!'),
				'level': 'danger',
			}, status=404)

		return func(telegram_bot_command=telegram_bot.commands.get(id=telegram_bot_command_id), *args, **kwargs)
	return wrapper

def check_telegram_bot_command_keyboard_button_id(func):
	@wraps(func)
	def wrapper(*args, **kwargs):
		telegram_bot_command: TelegramBotCommand = kwargs['telegram_bot_command']
		telegram_bot_command_keyboard: TelegramBotCommandKeyboard = telegram_bot_command.keyboard
		telegram_bot_command_keyboard_button_id: int = kwargs.pop('telegram_bot_command_keyboard_button_id')

		if not telegram_bot_command_keyboard.buttons.filter(id=telegram_bot_command_keyboard_button_id).exists():
			return Response({
				'message': _('Кнопка клавиатуры команды Telegram бота не найдена!'),
				'level': 'danger',
			}, status=404)

		return func(telegram_bot_command_keyboard_button=telegram_bot_command_keyboard.buttons.get(id=telegram_bot_command_keyboard_button_id), *args, **kwargs)
	return wrapper

def check_telegram_bot_user_id(func):
	def wrapper(*args, **kwargs):
		telegram_bot: TelegramBot = kwargs['telegram_bot']
		telegram_bot_user_id: int = kwargs.pop('telegram_bot_user_id')

		if not telegram_bot.users.filter(id=telegram_bot_user_id).exists():
			return Response({
				'message': _('Пользователь Telegram бота не найдена!'),
				'level': 'danger',
			}, status=404)

		return func(telegram_bot_user=telegram_bot.users.get(id=telegram_bot_user_id), *args, **kwargs)
	return wrapper
