from django.db.utils import OperationalError

from threading import Thread
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
