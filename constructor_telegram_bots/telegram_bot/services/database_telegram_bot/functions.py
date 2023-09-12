from pymongo import MongoClient
from pymongo.collection import Collection

from django.conf import settings

from typing import List, Union


def connect_to_database(func):
	def wrapper(telegram_bot, *args, **kwargs):
		client = MongoClient('127.0.0.1', 27017)
		collection = client.telegram_bots.get_collection('0' if settings.TEST else str(telegram_bot.id))
		result: Union[list, dict, None] = func(collection=collection, *args, **kwargs)
		client.close()

		return result
	return wrapper

@connect_to_database
def delete_collection(*, collection: Collection) -> None:
	collection.drop()

@connect_to_database
def insert_record(record: dict, *, collection: Collection) -> dict:
	if collection.count_documents({}) > 0:
		record_id = [record['_id'] for record in collection.find()][-1] + 1
	else:
		record_id = 1

	record.update({'_id': record_id})

	collection.insert_one(record)
	return collection.find_one({'_id': record['_id']})

@connect_to_database
def update_record(record_id: int, updated_record: dict, *, collection: Collection) -> dict:
	updated_record_ = {
		'$set': {},
		'$unset': {},
	}

	updated_record.update({'_id': record_id})
	old_record: dict = collection.find_one({'_id': record_id})

	for key, value in updated_record.items():
		if key in old_record and old_record[key] != value:
			updated_record_['$set'][key] = value
		else:
			updated_record_['$set'][key] = value

	for key in old_record:
		if key not in updated_record:
			updated_record_['$unset'][key] = 1

	collection.update_one({'_id': record_id}, updated_record_)
	return collection.find_one({'_id': record_id})

@connect_to_database
def delete_record(record_id: int, *, collection: Collection) -> None:
	collection.delete_one({'_id': record_id})

@connect_to_database
def get_records(*, collection: Collection) -> List[dict]:
	return [record for record in collection.find()]
