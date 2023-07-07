from telegram_bot.services.database_telegram_bot.decorators import connect_to_database

from telegram_bot.models import TelegramBot

from pymongo.collection import Collection


@connect_to_database
def insert_one_record(telegram_bot: TelegramBot, record: dict, *, collection: Collection) -> None:
	collection.insert_one(record)

@connect_to_database
def insert_many_records(telegram_bot: TelegramBot, records: list, *, collection: Collection) -> None:
	collection.insert_many(records)

@connect_to_database
def delete_one_record(telegram_bot: TelegramBot, record_id: int, *, collection: Collection) -> None:
	collection.delete_one({'_id': record_id})

@connect_to_database
def get_one_record(telegram_bot: TelegramBot, record_id: int, *, collection: Collection) -> dict:
	return collection.find_one({'_id': record_id})

@connect_to_database
def get_all_records(telegram_bot: TelegramBot, *, collection: Collection) -> list:
	return [record for record in collection.find()]
