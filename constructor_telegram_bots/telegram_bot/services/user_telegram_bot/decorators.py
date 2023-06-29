from aiogram import types

from django.db import models

from telegram_bot.models import (
	TelegramBot,
	TelegramBotUser,
	TelegramBotCommand,
	TelegramBotCommandManager
)

from telegram_bot.services.user_telegram_bot import functions

from asgiref.sync import sync_to_async
import aiohttp

from functools import wraps
from typing import Union
import re


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
		callback_query: types.CallbackQuery = kwargs['callback_query']

		if not callback_query:
			telegram_bot_commands: TelegramBotCommandManager = await sync_to_async(telegram_bot.commands.filter)(command=message.text)

			if await telegram_bot_commands.aexists():
				telegram_bot_command: TelegramBotCommand = await telegram_bot_commands.afirst()
			else:
				telegram_bot_command: Union[TelegramBotCommand, None] = await functions.search_telegram_bot_command(
					telegram_bot=telegram_bot,
					message_text=message.text
				)
		else:
			telegram_bot_command: Union[TelegramBotCommand, None] = await functions.search_telegram_bot_command(
				telegram_bot=telegram_bot,
				button_id=int(callback_query.data)
			)

		if not telegram_bot_command:
			async for telegram_bot_command_ in telegram_bot.commands.all():
				if (
					message.text == await functions.replace_text_variables(
						message=message,
						text=telegram_bot_command_.command
					)
				):
					telegram_bot_command = telegram_bot_command_
					break

		if telegram_bot_command:
			kwargs.update({'telegram_bot_command': telegram_bot_command})

			return await func(*args, **kwargs)
	return wrapper

def check_message_text(func):
	@wraps(func)
	async def wrapper(*args, **kwargs):
		message: types.Message = kwargs['message']
		telegram_bot_command: TelegramBotCommand = kwargs['telegram_bot_command']

		message_text: str = await functions.replace_text_variables(
			message=message,
			text=telegram_bot_command.message_text
		)

		if telegram_bot_command.api_request:
			async with aiohttp.ClientSession() as session:
				api_request_url: str = await functions.replace_text_variables(
					message=message,
					text=telegram_bot_command.api_request['url']
				)
				api_request_data: str = await functions.replace_text_variables(
					message=message,
					text=telegram_bot_command.api_request['data']
				)

				async with session.post(url=api_request_url, data=api_request_data) as response:
					message_text: str = message_text.replace('${api_response}', await response.text())

					variables: list = re.findall(r'\${([\w\[\]]+)}', message_text)

					if variables != []:
						for variable in variables:
							try:
								api_response_json_value = await response.json()
							except aiohttp.client_exceptions.ContentTypeError:
								message_text: str = message_text.replace('${' + variable + '}', 'The API-request not return JSON!')
								continue

							variable_keys: list = re.findall(r'\[([^\]]+)\]', variable)

							for variable_key in variable_keys:
								api_response_json_value = api_response_json_value[variable_key]

							message_text: str = message_text.replace('${' + variable + '}', str(api_response_json_value))

		if len(message_text) > 4096:
			message_text = 'The text of the message must contain no more than 4096 characters!'

		kwargs.update({'message_text': message_text})

		return await func(*args, **kwargs)
	return wrapper
