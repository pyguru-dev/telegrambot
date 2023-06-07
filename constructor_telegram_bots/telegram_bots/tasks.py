from celery import shared_task
from redis import Redis

from telegram_bot.models import TelegramBot

from telegram_bots import ConstructorTelegramBot
from telegram_bots import UserTelegramBot

from threading import Thread
from typing import Union


redis_client = Redis(host='127.0.0.1', port=6379)


@shared_task
def stop_telegram_bot(telegram_bot_id: int) -> None:
	telegram_bot: TelegramBot = TelegramBot.objects.get(id=telegram_bot_id)
	telegram_bot.is_running = False
	telegram_bot.save()

async def start_telegram_bot__(telegram_bot: Union[ConstructorTelegramBot, UserTelegramBot]) -> None:
	await telegram_bot.setup()
	await telegram_bot.start()

def start_telegram_bot_(telegram_bot: Union[ConstructorTelegramBot, UserTelegramBot]) -> None:
	telegram_bot.loop.run_until_complete(start_telegram_bot__(telegram_bot))
	telegram_bot.loop.stop()

@shared_task
def start_telegram_bot(telegram_bot_id: int) -> None:
	telegram_bot: TelegramBot = TelegramBot.objects.get(id=telegram_bot_id)
	telegram_bot.is_running = True
	telegram_bot.is_stopped = False
	telegram_bot.save()

	user_telegram_bot = UserTelegramBot(telegram_bot=telegram_bot)
	Thread(target=start_telegram_bot_, args=(user_telegram_bot,), daemon=True).start()

@shared_task
def start_all_telegram_bots() -> None:
	print(redis_client.get('is_all_telegram_bots_already_started'))
	if redis_client.get('is_all_telegram_bots_already_started') is None:
		constructor_telegram_bot = ConstructorTelegramBot()
		Thread(target=start_telegram_bot_, args=(constructor_telegram_bot,), daemon=True).start()

		for telegram_bot in TelegramBot.objects.all():
			if telegram_bot.is_running:
				start_telegram_bot.delay(telegram_bot_id=telegram_bot.id)

		redis_client.set('is_all_telegram_bots_already_started', '1'.encode('UTF-8'), ex=120)
