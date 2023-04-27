from django.db.utils import OperationalError

from telegram.error import InvalidToken, Unauthorized
from telegram.ext import Updater
from telegram import User

from threading import Thread
from typing import Union
import random
import os


def if_find_folder_or_file(directory: str, name: str) -> bool:
	for _name in os.listdir(directory):
		if _name == name:
			return True

	return False

def generator_secret_string(length: int, chars: str) -> str:
	secret_string = ''

	for num in range(length):
		secret_string += random.choice(chars)
	
	return secret_string

def check_telegram_bot_token(token: str) -> Union[User, None]:
	try:
		updater = Updater(token=token)
		bot = updater.bot.get_me()

		return bot
	except (InvalidToken, Unauthorized):
		return None

def start_all_telegram_bots() -> None:
	from telegram_bot.models import TelegramBot

	from scripts.constructor_telegram_bot import ConstructorTelegramBot
	from scripts.user_telegram_bot import UserTelegramBot

	constructor_telegram_bot = ConstructorTelegramBot()
	Thread(target=constructor_telegram_bot.start, daemon=True).start()

	try:
		for telegram_bot in TelegramBot.objects.all():
			if telegram_bot.is_running:
				user_telegram_bot = UserTelegramBot(telegram_bot=telegram_bot)
				Thread(target=user_telegram_bot.start, daemon=True).start()
	except OperationalError:
		pass
