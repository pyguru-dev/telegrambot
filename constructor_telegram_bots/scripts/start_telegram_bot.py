from scripts.constructor_telegram_bot import ConstructorTelegramBot
from scripts.user_telegram_bot import UserTelegramBot

from telegram_bot.models import TelegramBot

from asyncio import AbstractEventLoop
import asyncio

from threading import Thread
from typing import Union


async def start_bot(telegram_bot: Union[ConstructorTelegramBot, UserTelegramBot]) -> None:
	await telegram_bot.setup()
	await telegram_bot.start()

def start_telegram_bot(telegram_bot: Union[ConstructorTelegramBot, UserTelegramBot]) -> None:
	telegram_bot.loop: AbstractEventLoop = asyncio.new_event_loop()
	Thread(target=telegram_bot.loop.run_until_complete, args=(start_bot(telegram_bot),), daemon=True).start()

def start_all_telegram_bots() -> None:
	constructor_telegram_bot = ConstructorTelegramBot()
	start_telegram_bot(telegram_bot=constructor_telegram_bot)
	for telegram_bot in TelegramBot.objects.all():
		if telegram_bot.is_running:
			user_telegram_bot = UserTelegramBot(telegram_bot=telegram_bot)
			start_telegram_bot(telegram_bot=user_telegram_bot)
