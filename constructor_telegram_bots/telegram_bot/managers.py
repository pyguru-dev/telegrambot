from django.core.handlers.wsgi import WSGIRequest
from django.db import models

import telegram_bot.models as TelegramBotModels

import constructor_telegram_bots.functions as Functions


class TelegramBotManager(models.Manager):
	def add_telegram_bot(self, request: WSGIRequest, api_token: str, private: bool, **extra_fields):
		username: str = Functions.check_telegram_bot_api_token(api_token=api_token)

		telegram_bot: TelegramBotModels.TelegramBot = self.model(name=username, api_token=api_token, private=private, **extra_fields)
		telegram_bot.save()

		request.user.telegram_bots.add(telegram_bot)
		request.user.save()

		return telegram_bot


class TelegramBotCommandManager(models.Manager):
	def add_telegram_bot_command(self, telegram_bot, name: str, command: str, callback: str, message_text: str, keyboard: str, **extra_fields):
		telegram_bot_command: TelegramBotModels.TelegramBotCommand = self.model(
			name=name,
			command=command,
			callback=callback,
			message_text=message_text,
			keyboard=keyboard,
			**extra_fields
		)
		telegram_bot_command.save()

		telegram_bot.commands.add(telegram_bot_command)
		telegram_bot.save()

		return telegram_bot_command
