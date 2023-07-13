from aiogram import types

from django.db import models
from telegram_bot.models import (
	TelegramBot,
	TelegramBotUser,
	TelegramBotCommand,
	TelegramBotCommandManager
)

from constructor_telegram_bots import environment
from telegram_bot.services import database_telegram_bot
from telegram_bot.services.user_telegram_bot.functions import search_telegram_bot_command, get_text_variables

from asgiref.sync import sync_to_async
import aiohttp

from functools import wraps
from typing import List, Union
import json


def check_request(func):
	@wraps(func)
	async def wrapper(*args, **kwargs):
		if isinstance(args[1], types.Message):
			message: types.Message = args[1]

			kwargs.update(
				{
					'message': message,
					'callback_query': None,
					'user_id': message.from_user.id,
					'user_full_name': message.from_user.full_name,
				}
			)
		else:
			callback_query: types.CallbackQuery = args[1]
			message: types.Message = callback_query.message

			kwargs.update(
				{
					'message': message,
					'callback_query': callback_query,
					'user_id': callback_query.from_user.id,
					'user_full_name': callback_query.from_user.full_name,
				}
			)

		return await func(args[0], **kwargs)
	return wrapper

def check_telegram_bot_user(func):
	@wraps(func)
	async def wrapper(*args, **kwargs):
		telegram_bot: TelegramBot = args[0].telegram_bot

		user_id: int = kwargs.pop('user_id')
		user_full_name: str = kwargs.pop('user_full_name')

		telegram_bot_users: models.Manager = await sync_to_async(TelegramBotUser.objects.filter)(user_id=user_id)

		if not await telegram_bot_users.aexists():
			telegram_bot_user: TelegramBotUser = await sync_to_async(TelegramBotUser.objects.create)(
				telegram_bot=telegram_bot,
				user_id=user_id,
				full_name=user_full_name
			)
		else:
			telegram_bot_user: TelegramBotUser = await telegram_bot_users.afirst()
			telegram_bot_user.full_name = user_full_name
			await telegram_bot_user.asave()

		if telegram_bot.is_private and telegram_bot_user.is_allowed or not telegram_bot.is_private:
			return await func(*args, **kwargs)
	return wrapper

def check_telegram_bot_command(func):
	@wraps(func)
	async def wrapper(*args, **kwargs):
		telegram_bot: TelegramBot = args[0].telegram_bot

		message: types.Message = kwargs['message']
		callback_query: Union[types.CallbackQuery, None] = kwargs['callback_query']

		if not callback_query:
			telegram_bot_commands: TelegramBotCommandManager = await sync_to_async(telegram_bot.commands.filter)(command=message.text)

			if await telegram_bot_commands.aexists():
				telegram_bot_command: TelegramBotCommand = await telegram_bot_commands.afirst()
			else:
				telegram_bot_command: Union[TelegramBotCommand, None] = await search_telegram_bot_command(
					telegram_bot=telegram_bot,
					message_text=message.text
				)
		else:
			telegram_bot_command: Union[TelegramBotCommand, None] = await search_telegram_bot_command(
				telegram_bot=telegram_bot,
				button_id=int(callback_query.data)
			)

		if not telegram_bot_command:
			text_variables: dict = await get_text_variables(telegram_bot, message, callback_query)

			async for telegram_bot_command_ in telegram_bot.commands.all():
				if (message.text == await sync_to_async(environment.replace_text_variables)(telegram_bot, telegram_bot_command_.command, text_variables)):
					telegram_bot_command = telegram_bot_command_
					break

		if telegram_bot_command:
			kwargs.update({'telegram_bot_command': telegram_bot_command})

			return await func(*args, **kwargs)
	return wrapper

def check_telegram_bot_command_database_record(func):
	@wraps(func)
	async def wrapper(*args, **kwargs):
		self = args[0]
		message: types.Message = kwargs['message']
		callback_query: Union[types.CallbackQuery, None] = kwargs['callback_query']
		telegram_bot_command: TelegramBotCommand = kwargs['telegram_bot_command']

		if telegram_bot_command.database_record is not None:
			text_variables: dict = await get_text_variables(self.telegram_bot, message, callback_query)

			for key, value in text_variables.items():
				text_variables[key] = f'"{value}"'

			database_error_record = {'message': 'Failed to write record to database!'}

			try:
				database_record: str = await sync_to_async(environment.replace_text_variables)(self.telegram_bot, telegram_bot_command.database_record, text_variables)
				database_record: Union[list, dict] = json.loads(database_record)
			except:
				database_record = database_error_record

			if not isinstance(database_record, dict):
				database_record = database_error_record

			database_telegram_bot.insert_one_record(self.telegram_bot, database_record)

		return await func(*args, **kwargs)
	return wrapper


def check_message_text(func):
	@wraps(func)
	async def wrapper(*args, **kwargs):
		self = args[0]
		message: types.Message = kwargs['message']
		callback_query: Union[types.CallbackQuery, None] = kwargs['callback_query']
		telegram_bot_command: TelegramBotCommand = kwargs['telegram_bot_command']

		text_variables: dict = await get_text_variables(self.telegram_bot, message, callback_query)

		if telegram_bot_command.api_request:
			try:
				async with aiohttp.ClientSession() as session:
					url: str = await sync_to_async(environment.replace_text_variables)(self.telegram_bot, telegram_bot_command.api_request['url'], text_variables)
					data: str = await sync_to_async(environment.replace_text_variables)(self.telegram_bot, telegram_bot_command.api_request['data'], text_variables)

					async with session.post(url, data=data) as response:
						try:
							response_json: Union[list, dict] = await response.json()
							text_variables.update({'api_response': response_json})
						except aiohttp.client_exceptions.ContentTypeError:
							text_variables.update({'api_response': 'API-request return not JSON!'})
			except aiohttp.client_exceptions.InvalidURL:
				text_variables.update({'api_response': 'URL is invalid!'})

		message_text: str = await sync_to_async(environment.replace_text_variables)(self.telegram_bot, telegram_bot_command.message_text, text_variables)

		if len(message_text) > 4096:
			message_text = 'The message text must contain no more than 4096 characters!'

		return await func(message_text=message_text, *args, **kwargs)
	return wrapper
