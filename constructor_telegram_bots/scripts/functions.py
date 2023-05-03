from django.db.utils import OperationalError

from telegram.error import InvalidToken, Unauthorized
from telegram.ext import Updater
from telegram import User

from threading import Thread
from typing import Union
import random


def generator_secret_string(length: int, chars: str) -> str:
	secret_string = ''
	for num in range(length):
		secret_string += random.choice(chars)
	return secret_string

def check_telegram_bot_token(token: str) -> Union[User, None]:
	try:
		updater = Updater(token=token)
		return updater.bot.get_me()
	except (InvalidToken, Unauthorized):
		return None

def start_all_telegram_bots() -> None:
	# from telegram_bot.models import TelegramBot

	import scripts.constructor_telegram_bot as ConstructorTelegramBot
	# from scripts.user_telegram_bot import UserTelegramBot

	import asyncio


	async def start_all_bots() -> None:
		task = asyncio.create_task(ConstructorTelegramBot.start())
		await asyncio.gather(task)


	loop = asyncio.new_event_loop()
	asyncio.set_event_loop(loop)
	Thread(target=loop.run_until_complete, args=(start_all_bots(),)).start()

	# try:
	# 	for telegram_bot in TelegramBot.objects.all():
	# 		if telegram_bot.is_running:
	# 			user_telegram_bot = UserTelegramBot(telegram_bot=telegram_bot)
	# 			Thread(target=user_telegram_bot.start, daemon=True).start()
	# except OperationalError:
	# 	pass
