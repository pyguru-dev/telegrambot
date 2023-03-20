#!/usr/bin/env python

import os
import sys

import scripts.functions as Functions

def main() -> None:
	"""Run administrative tasks."""
	os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'constructor_telegram_bots.settings')
	try:
		from django.core.management import execute_from_command_line
	except ImportError as exc:
		raise ImportError(
			"Couldn't import Django. Are you sure it's installed and "
			"available on your PYTHONPATH environment variable? Did you "
			"forget to activate a virtual environment?"
		) from exc

	if sys.argv[1] == 'runserver':
		# SECURITY WARNING: keep the constructor_telegram_bot.py token used in production secret!
		if Functions.if_find_folder_or_file('./data', 'constructor_telegram_bot.token') == False:
			open('./data/constructor_telegram_bot.token', 'w')

			print('Enter the Constructor Telegram bot token in the file ./data/constructor_telegram_bot.token!')
		else:
			with open('./data/constructor_telegram_bot.token', 'r') as constructor_telegram_bot_token_file:
				constructor_telegram_bot_token = constructor_telegram_bot_token_file.read()

			if constructor_telegram_bot_token == '':
				print('Enter the Constructor Telegram bot token in the file ./data/constructor_telegram_bot.token!')
			else:
				execute_from_command_line(sys.argv)
	else:
		execute_from_command_line(sys.argv)

if __name__ == '__main__':
	main()