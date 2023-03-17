from threading import Thread
import random
import os

def if_find_folder_or_file(directory: str, name: str):
	is_find_name = False
	for i in os.listdir(directory):
		if i == name:
			is_find_name = True

	return is_find_name

def generator_secret_string(length: int, chars: str):
	secret_string = ''
	for i in range(length):
		secret_string += random.choice(chars)
	
	return secret_string

def start_all_telegram_bots():
	from scripts.constructor_telegram_bot import ConstructorTelegramBot

	constructor_telegram_bot = ConstructorTelegramBot()
	th = Thread(target=constructor_telegram_bot.start, daemon=True)
	th.start()