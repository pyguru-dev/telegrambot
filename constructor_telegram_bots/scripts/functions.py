from asyncio import AbstractEventLoop
import asyncio

from requests import Response
import requests

from threading import Thread
from typing import Union
import random
import json


def generator_random_string(length: int, chars: str) -> str:
	random_string = ''

	for num in range(length):
		random_string += random.choice(chars)

	return random_string

def check_telegram_bot_api_token(api_token: str) -> Union[str, None]:
	responce = requests.get(url=f'https://api.telegram.org/bot{api_token}/getMe')

	if responce.status_code == 200:
		responce_json: dict = json.loads(responce.text)
		return responce_json['result']['username']
	else:
		return None

async def start_bot(telegram_bot) -> None:
	await telegram_bot.setup()
	await telegram_bot.start()

def start_telegram_bot(telegram_bot) -> None:
	telegram_bot.loop: AbstractEventLoop = asyncio.new_event_loop()
	Thread(target=telegram_bot.loop.run_until_complete, args=(start_bot(telegram_bot),), daemon=True).start()

def start_all_telegram_bots() -> None:
	from telegram_bot.models import TelegramBot

	from scripts.constructor_telegram_bot import ConstructorTelegramBot
	from scripts.user_telegram_bot import UserTelegramBot


	constructor_telegram_bot = ConstructorTelegramBot()
	start_telegram_bot(telegram_bot=constructor_telegram_bot)
	for telegram_bot in TelegramBot.objects.all():
		if telegram_bot.is_running:
			user_telegram_bot = UserTelegramBot(telegram_bot=telegram_bot)
			start_telegram_bot(telegram_bot=user_telegram_bot)
