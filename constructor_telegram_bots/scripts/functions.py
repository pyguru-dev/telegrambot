from aiogram.utils.exceptions import TerminatedByOtherGetUpdates

from threading import Thread
from typing import Union
import requests
import asyncio
import random
import json


def generator_secret_string(length: int, chars: str) -> str:
	secret_string = ''
	for num in range(length):
		secret_string += random.choice(chars)
	return secret_string

def check_telegram_bot_token(token: str) -> Union[str, None]:
	responce = requests.get(url=f'https://api.telegram.org/bot{token}/getMe')
	if responce.status_code == 200:
		responce_json = json.loads(responce.text)
		return responce_json['result']['username']
	else:
		return None

async def start_bot(telegram_bot) -> None:
	await telegram_bot.start()

def start_telegram_bot(telegram_bot) -> None:
	loop = asyncio.new_event_loop()
	Thread(target=loop.run_until_complete, args=(start_bot(telegram_bot),), daemon=True).start()

def start_all_telegram_bots() -> None:
	from telegram_bot.models import TelegramBot

	import scripts.constructor_telegram_bot as ConstructorTelegramBot
	from scripts.user_telegram_bot import UserTelegramBot


	start_telegram_bot(telegram_bot=ConstructorTelegramBot)
	for telegram_bot in TelegramBot.objects.all():
		if telegram_bot.is_running:
			user_telegram_bot = UserTelegramBot(telegram_bot=telegram_bot)
			start_telegram_bot(telegram_bot=user_telegram_bot)
