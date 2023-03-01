from django.core.handlers.wsgi import WSGIRequest
from django.db import models

from telegram.ext import Updater
from telegram.error import InvalidToken

class TelegramBotManager(models.Manager):
	def test_telegram_bot_token(self, token: str):
		try:
			return Updater(token=token)
		except InvalidToken:
			return None

	def add_telegram_bot(self, request: WSGIRequest, token: str, private: bool, **extra_fields):
		updater = Updater(token=token)
		bot = updater.bot.get_me()

		telegram_bot = self.model(name=bot.username, token=token, private=private, **extra_fields)
		telegram_bot.save()

		request.user.telegram_bots.add(telegram_bot)
		request.user.save()

		return telegram_bot