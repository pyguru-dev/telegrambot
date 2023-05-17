from telegram_bots.constructor_telegram_bot import ConstructorTelegramBot
from telegram_bots.user_telegram_bot import UserTelegramBot

from telegram_bot.models import TelegramBot

from threading import Thread
from typing import Union


async def start_telegram_bot_step_2(telegram_bot: Union[ConstructorTelegramBot, UserTelegramBot]) -> None:
	await telegram_bot.setup()
	await telegram_bot.start()

def start_telegram_bot_step_1(telegram_bot: Union[ConstructorTelegramBot, UserTelegramBot]) -> None:
	telegram_bot.loop.run_until_complete(start_telegram_bot_step_2(telegram_bot))
	telegram_bot.loop.stop()

def start_telegram_bot(telegram_bot: Union[ConstructorTelegramBot, UserTelegramBot]) -> None:
	Thread(target=start_telegram_bot_step_1, args=(telegram_bot,), daemon=True).start()

def start_all_telegram_bots() -> None:
	constructor_telegram_bot = ConstructorTelegramBot()
	start_telegram_bot(telegram_bot=constructor_telegram_bot)
	for telegram_bot in TelegramBot.objects.all():
		if telegram_bot.is_running:
			user_telegram_bot = UserTelegramBot(telegram_bot=telegram_bot)
			start_telegram_bot(telegram_bot=user_telegram_bot)
