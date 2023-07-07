from telegram_bot.models import TelegramBot

from pymongo import MongoClient
from typing import Union


def connect_to_database(func):
	def wrapper(telegram_bot: TelegramBot, *args, **kwargs):
		client = MongoClient('127.0.0.1', 27017)
		collection = client.telegram_bots.get_collection(str(telegram_bot.id))
		result: Union[list, dict, None] = func(telegram_bot, collection=collection, *args, **kwargs)
		client.close()

		return result
	return wrapper
