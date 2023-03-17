from django.core.handlers.wsgi import WSGIRequest
from django.db import models

from telegram.ext import Updater
from telegram.error import InvalidToken

import telegram_bot.models as TelegramBotModels

class TelegramBotManager(models.Manager):
	def test_telegram_bot_token(self, token: str):
		try:
			return Updater(token=token)
		except InvalidToken:
			return None

	def add_telegram_bot(self, request: WSGIRequest, token: str, private: bool, **extra_fields):
		updater = Updater(token=token)
		bot = updater.bot.get_me()

		telegram_bot: TelegramBotModels.TelegramBot = self.model(name=bot.username, token=token, private=private, **extra_fields)
		telegram_bot.save()

		request.user.telegram_bots.add(telegram_bot)
		request.user.save()

		return telegram_bot
	
	def duplicate_telegram_bot(self, request: WSGIRequest, telegram_bot, token: str, private: bool, **extra_fields):
		duplicated_telegram_bot: TelegramBotModels.TelegramBot = self.add_telegram_bot(request=request, token=token, private=private, **extra_fields)

		for telegram_bot_command in telegram_bot.commands.all():
			TelegramBotModels.TelegramBotCommand.objects.add_telegram_bot_command(telegram_bot=duplicated_telegram_bot, name=telegram_bot_command.name, command=telegram_bot_command.command, callback=telegram_bot_command.callback, message_text=telegram_bot_command.message_text, is_edit_last_message=telegram_bot_command.is_edit_last_message, keyboard=telegram_bot_command.keyboard)

	def delete_telegram_bot(self, telegram_bot):
		for telegram_bot_command in telegram_bot.commands.all():
			telegram_bot_command.delete()

		for telegram_bot_user in telegram_bot.users.all():
			telegram_bot_user.delete()

		telegram_bot.delete()

class TelegramBotCommandManager(models.Manager):
	def add_telegram_bot_command(self, telegram_bot, name: str, command: str, callback: str, message_text: str, is_edit_last_message: bool, keyboard: str, **extra_fields):
		telegram_bot_command: TelegramBotModels.TelegramBotCommand = self.model(name=name, command=command, callback=callback, message_text=message_text, is_edit_last_message=is_edit_last_message, keyboard=keyboard, **extra_fields)
		telegram_bot_command.save()

		telegram_bot.commands.add(telegram_bot_command)
		telegram_bot.save()