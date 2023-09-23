from aiogram import types

from django.db import models

from constructor_telegram_bots import environment

from telegram_bot.models import *
from telegram_bot.services import database_telegram_bot

from .functions import search_telegram_bot_command, get_text_variables

from asgiref.sync import sync_to_async
import aiohttp

from functools import wraps
from typing import Optional, Union
import json


def check_telegram_bot_user(func):
	@wraps(func)
	async def wrapper(self, request: Union[types.Message, types.CallbackQuery], *args, **kwargs):
		telegram_bot: TelegramBot = self.telegram_bot
		telegram_bot_user_: models.Manager = await sync_to_async(telegram_bot.users.filter)(user_id=request.from_user.id)

		if not await telegram_bot_user_.aexists():
			telegram_bot_user: TelegramBotUser = await TelegramBotUser.objects.acreate(
				telegram_bot=telegram_bot,
				user_id=request.from_user.id,
				full_name=request.from_user.full_name
			)
		else:
			telegram_bot_user: TelegramBotUser = await telegram_bot_user_.afirst()

		if not telegram_bot.is_private or telegram_bot.is_private and telegram_bot_user.is_allowed:
			return await func(self, request, *args, **kwargs)
	return wrapper

def check_telegram_bot_command(func):
	@wraps(func)
	async def wrapper(self, request: Union[types.Message, types.CallbackQuery], *args, **kwargs):
		telegram_bot_command = None

		if isinstance(request, types.Message):
			text_variables: dict = await get_text_variables(telegram_bot=self.telegram_bot, request=request)

			async for telegram_bot_command_ in self.telegram_bot.commands.all():
				telegram_bot_command_command: Optional[TelegramBotCommandCommand] = await telegram_bot_command_.aget_command()

				if telegram_bot_command_command:
					telegram_bot_command_command_command: str = await environment.areplace_text_variables(
						telegram_bot=self.telegram_bot,
						text=telegram_bot_command_command.text,
						text_variables=text_variables
					)

					if telegram_bot_command_command_command == request.text:
						telegram_bot_command: TelegramBotCommand = telegram_bot_command_
				else:
					telegram_bot_command: Optional[TelegramBotCommand] = await search_telegram_bot_command(
						telegram_bot=self.telegram_bot,
						message_text=request.text
					)

				if telegram_bot_command:
					break
		elif isinstance(request, types.CallbackQuery) and request.data.isdigit():
			telegram_bot_command: Optional[TelegramBotCommand] = await search_telegram_bot_command(
				telegram_bot=self.telegram_bot,
				button_id=int(request.data)
			)

		if telegram_bot_command:
			return await func(self, request, telegram_bot_command=telegram_bot_command, *args, **kwargs)
	return wrapper

def check_telegram_bot_command_database_record(func):
	@wraps(func)
	async def wrapper(self, request: Union[types.Message, types.CallbackQuery], *args, **kwargs):
		telegram_bot_command: TelegramBotCommand = kwargs['telegram_bot_command']

		if telegram_bot_command.database_record:
			text_variables: dict = await get_text_variables(telegram_bot=self.telegram_bot, request=request)
			database_record: dict = await environment.areplace_text_variables(
				telegram_bot=self.telegram_bot,
				text=telegram_bot_command.database_record,
				text_variables=text_variables
			)

			database_telegram_bot.insert_record(self.telegram_bot, database_record)
		return await func(self, request, *args, **kwargs)
	return wrapper

def check_message_text(func):
	@wraps(func)
	async def wrapper(self, request: Union[types.Message, types.CallbackQuery], *args, **kwargs):
		telegram_bot_command: TelegramBotCommand = kwargs['telegram_bot_command']
		telegram_bot_command_api_request: TelegramBotCommandApiRequest = await telegram_bot_command.aget_api_request()
		text_variables: dict = await get_text_variables(telegram_bot=self.telegram_bot, request=request)

		if telegram_bot_command_api_request:
			async with aiohttp.ClientSession() as session:
				method: str = telegram_bot_command_api_request.method
				url: str = await environment.areplace_text_variables(
					telegram_bot=self.telegram_bot,
					text=telegram_bot_command_api_request.url,
					text_variables=text_variables
				)

				if telegram_bot_command_api_request.headers:
					headers: dict = await environment.areplace_text_variables(
						telegram_bot=self.telegram_bot,
						text=json.dumps(telegram_bot_command_api_request.headers),
						text_variables=text_variables
					)
				else:
					headers = None

				if telegram_bot_command_api_request.data:
					data: dict = await environment.areplace_text_variables(
						telegram_bot=self.telegram_bot,
						text=json.dumps(telegram_bot_command_api_request.data),
						text_variables=text_variables
					)
				else:
					data = None

				try:
					async with session.request(method=method, url=url, headers=headers, json=data) as response:
						try:
							text_variables['api_response'] = await response.json()
						except aiohttp.client_exceptions.ContentTypeError:
							text_variables['api_response'] = 'API-request return not JSON!'
				except aiohttp.client_exceptions.InvalidURL:
					text_variables['api_response'] = 'URL is invalid!'

		telegram_bot_command_message_text: TelegramBotCommandMessageText = await telegram_bot_command.aget_message_text()
		message_text: str = await environment.areplace_text_variables(
			telegram_bot=self.telegram_bot,
			text=telegram_bot_command_message_text.text,
			text_variables=text_variables
		)

		if len(message_text) > 4096:
			message_text = 'The message text must contain no more than 4096 characters!'

		return await func(self, request, message_text=message_text, *args, **kwargs)
	return wrapper
