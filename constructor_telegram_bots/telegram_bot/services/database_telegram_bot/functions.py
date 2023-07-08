from telegram_bot.services.database_telegram_bot.decorators import connect_to_database

from telegram_bot.models import TelegramBot

from pymongo.collection import Collection


@connect_to_database
def insert_one_record(telegram_bot: TelegramBot, record: dict, *, collection: Collection) -> None:
	record.update({'_id': collection.count_documents({}) + 1})
	collection.insert_one(record)

@connect_to_database
def insert_many_records(telegram_bot: TelegramBot, records: list[dict], *, collection: Collection) -> None:
	for record_num in range(len(records)):
		records[record_num].update({'_id': collection.count_documents({}) + 1 + record_num})

	collection.insert_many(records)

@connect_to_database
def delete_one_record(telegram_bot: TelegramBot, record_id: int, *, collection: Collection) -> None:
	collection.delete_one({'_id': record_id})

@connect_to_database
def get_one_record(telegram_bot: TelegramBot, record_id: int, *, collection: Collection) -> dict:
	return collection.find_one({'_id': record_id})

@connect_to_database
def get_all_records(telegram_bot: TelegramBot, *, collection: Collection) -> list[dict]:
	return [record for record in collection.find()]
