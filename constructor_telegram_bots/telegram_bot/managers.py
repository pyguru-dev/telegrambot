from django.db import models

from django.core.files.uploadedfile import InMemoryUploadedFile

import telegram_bot.models as TelegramBotModels
from user.models import User

from telegram_bot.functions import check_telegram_bot_api_token

from typing import Any, Union


class TelegramBotManager(models.Manager):
	def create(
		self,
	    owner: User,
		api_token: str,
		is_private: bool,
		**extra_fields: Any
	) -> 'TelegramBotModels.TelegramBot':
		name: str = check_telegram_bot_api_token(api_token=api_token)

		return super().create(
			owner=owner,
			name=name,
			api_token=api_token,
			is_private=is_private,
			**extra_fields
		)


class TelegramBotCommandManager(models.Manager):
	def create(
		self,
		telegram_bot: 'TelegramBotModels.TelegramBot',
		name: str,
		message_text: str,
		command: Union[str, None] = None,
		image: Union[InMemoryUploadedFile, None] = None,
		keyboard: Union[dict, None] = None,
		api_request: Union[list, None] = None,
		**extra_fields: Any
	) -> 'TelegramBotModels.TelegramBotCommand':
		telegram_bot_command: TelegramBotModels.TelegramBotCommand = super().create(
			telegram_bot=telegram_bot,
			name=name,
			command=command,
			image=image,
			message_text=message_text,
			api_request=api_request,
			**extra_fields
		)

		if keyboard is not None:
			TelegramBotModels.TelegramBotCommandKeyboard.objects.create(
				telegram_bot_command=telegram_bot_command,
				type=keyboard['type'],
				buttons=keyboard['buttons']
			)

		return telegram_bot_command


class TelegramBotCommandKeyboardManager(models.Manager):
	def create(
		self,
		telegram_bot_command: 'TelegramBotModels.TelegramBotCommand',
		type: str,
		buttons: dict,
		**extra_fields: Any
	) -> 'TelegramBotModels.TelegramBotCommandKeyboard':
		telegram_bot_command_keyboard: TelegramBotModels.TelegramBotCommandKeyboard = super().create(
			telegram_bot_command=telegram_bot_command,
			type=type,
			**extra_fields
		)

		for button in buttons:
			TelegramBotModels.TelegramBotCommandKeyboardButton.objects.create(
				telegram_bot_command_keyboard=telegram_bot_command_keyboard,
				text=button['text']
			)

		return telegram_bot_command_keyboard

class TelegramBotUserManager(models.Manager):
	def create(
		self,
		telegram_bot: 'TelegramBotModels.TelegramBot',
		user_id: int,
		username: str,
		**extra_fields: Any
	) -> 'TelegramBotModels.TelegramBotUser': 
		return super().create(
			telegram_bot=telegram_bot,
			user_id=user_id,
			username=username,
			**extra_fields
		)
