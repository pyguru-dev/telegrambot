from aiogram import Bot, types
from telegram_bots.custom_aiogram import CustomDispatcher

from aiogram.utils.exceptions import ValidationError, Unauthorized

from telegram_bot.models import (
	TelegramBot,
	TelegramBotCommand, TelegramBotCommandManager,
	TelegramBotCommandKeyboard,
	TelegramBotCommandKeyboardButton,
	TelegramBotUser
)
from django.db import models

from asgiref.sync import sync_to_async
import asyncio
import aiohttp

from typing import Union
import re


class UserTelegramBot:
	def __init__(self, telegram_bot: TelegramBot) -> None:
		self.telegram_bot = telegram_bot
		self.loop = asyncio.new_event_loop()

	async def check_user(self, user_id: int, full_name: str) -> TelegramBotUser:
		users: models.Manager = await sync_to_async(TelegramBotUser.objects.filter)(user_id=user_id)

		if await users.aexists() is False:
			user: TelegramBotUser = await sync_to_async(TelegramBotUser.objects.create)(
				telegram_bot=self.telegram_bot,
				user_id=user_id,
				full_name=full_name
			)
		else:
			user: TelegramBotUser = await users.afirst()
			user.full_name = full_name
			await user.asave()

		return user

	def get_command_keyboard_button_command(sefl, button: TelegramBotCommandKeyboardButton) -> TelegramBotCommand:
		return button.telegram_bot_command

	async def search_command(self, message_text: str = None, button_id: int = None) -> Union[TelegramBotCommand, None]:
		command = None

		async for command_ in self.telegram_bot.commands.all():
			if command is not None:
				break

			keyboard: TelegramBotCommandKeyboard = await sync_to_async(command_.get_keyboard)()

			if keyboard is not None:
				if keyboard.type == 'default' and message_text is not None or keyboard.type == 'inline' and button_id is not None:
					async for button in keyboard.buttons.all():
						if button.text == message_text and message_text is not None or button.id == button_id and button_id is not None:
							command: TelegramBotCommand = await sync_to_async(self.get_command_keyboard_button_command)(button=button)
							break

		return command
	
	async def get_command(self, message_text: str = None, button_id: int = None) -> Union[TelegramBotCommand, None]:
		if message_text is not None:
			commands: TelegramBotCommandManager = await sync_to_async(self.telegram_bot.commands.filter)(command=message_text)

			if await commands.aexists():
				command: TelegramBotCommand = await commands.afirst()
			else:
				command: Union[TelegramBotCommand, None] = await self.search_command(message_text=message_text)
		else:
			command: Union[TelegramBotCommand, None] = await self.search_command(button_id=button_id)

		return command

	async def replace_text_variables(self, message: types.Message, text: str) -> str:
		text_variables = {
			'${user_id}': message.from_user.id,
			'${user_username}': message.from_user.username,
			'${user_first_name}': message.from_user.first_name,
			'${user_last_name}': message.from_user.last_name,
			'${user_message_id}': message.message_id,
			'${user_message_text}': message.text,
		}

		for key, value in text_variables.items():
			text: str = text.replace(key, str(value))

		return text

	async def get_keyboard(self, command: TelegramBotCommand) -> Union[types.ReplyKeyboardMarkup, types.InlineKeyboardMarkup]:
		keyboard: TelegramBotCommandKeyboard =  await sync_to_async(command.get_keyboard)()
				
		if keyboard is not None:
			tg_keyboard_buttons = {}

			for num in range(await keyboard.buttons.acount()):
				tg_keyboard_buttons.update(
					{
						num + 1: [],
					}
				)

			tg_keyboard_row = 1

			if keyboard.type == 'default':
				tg_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)

				async for button in keyboard.buttons.all():
					tg_keyboard_buttons[tg_keyboard_row if button.row is None else button.row].append(
						types.KeyboardButton(text=button.text)
					)

					tg_keyboard_row += 1
			else:
				tg_keyboard = types.InlineKeyboardMarkup()

				async for button in keyboard.buttons.all():
					tg_keyboard_buttons[tg_keyboard_row if button.row is None else button.row].append(
						types.InlineKeyboardButton(
							text=button.text,
							url=button.url,
							callback_data=button.id
						)
					)

					tg_keyboard_row += 1

			for tg_keyboard_button in tg_keyboard_buttons:
				tg_keyboard.add(*tg_keyboard_buttons[tg_keyboard_button])
		else:
			tg_keyboard = None

		return tg_keyboard

	async def message_and_callback_query_handler(self, *args, **kwargs) -> None:
		if isinstance(args[0], types.Message):
			message: types.Message = args[0]

			user_id: int = message.from_user.id
			full_name: str = message.from_user.full_name
		else:
			callback_query: types.CallbackQuery = args[0]
			message: types.Message = callback_query.message

			user_id: int = callback_query.from_user.id
			full_name: str = callback_query.from_user.full_name

		user: TelegramBotUser = await self.check_user(user_id=user_id, full_name=full_name)

		if self.telegram_bot.is_private and user.is_allowed or self.telegram_bot.is_private is False:
			if isinstance(args[0], types.Message):
				command: TelegramBotCommand = await self.get_command(message_text=message.text)
			else:
				command: TelegramBotCommand = await self.get_command(button_id=int(callback_query.data))

			if command is not None:
				message_text: str = await self.replace_text_variables(message=message, text=command.message_text)

				if command.api_request is not None:
					async with aiohttp.ClientSession() as session:
						api_request_url: str = await self.replace_text_variables(message=message, text=command.api_request['url'])
						api_request_data: str = await self.replace_text_variables(message=message, text=command.api_request['data'])

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

				keyboard: Union(types.ReplyKeyboardMarkup, types.InlineKeyboardMarkup) = await self.get_keyboard(command=command)

				if isinstance(args[0], types.CallbackQuery):
					await self.dispatcher.bot.delete_message(
						chat_id=message.chat.id,
						message_id=message.message_id
					)

				if command.image == '':
					await self.dispatcher.bot.send_message(
						chat_id=message.chat.id,
						text=message_text,
						reply_markup=keyboard
					)
				else:
					await self.dispatcher.bot.send_photo(
						chat_id=message.chat.id,
						photo=types.InputFile(command.image.path),
						caption=message_text,
						reply_markup=keyboard
					)

	async def setup(self) -> None:
		self.bot = Bot(token=self.telegram_bot.api_token, loop=self.loop)
		self.dispatcher = CustomDispatcher(bot_username=self.telegram_bot.name, bot=self.bot)

		self.dispatcher.register_message_handler(self.message_and_callback_query_handler)
		self.dispatcher.register_callback_query_handler(self.message_and_callback_query_handler)

	async def start(self) -> None:
		task = self.loop.create_task(self.stop())

		try:
			await self.dispatcher.skip_updates()
			await self.dispatcher.start_polling()

			task.cancel()

			self.telegram_bot.is_stopped = True
			await self.telegram_bot.asave()
		except (ValidationError, Unauthorized):
			task.cancel()

			await self.telegram_bot.adelete()

		session = await self.bot.get_session()
		await session.close()

	async def stop(self) -> None:
		while self.telegram_bot.is_running:
			self.telegram_bot: TelegramBot = await TelegramBot.objects.aget(id=self.telegram_bot.id)

			if self.telegram_bot.is_running is False:
				self.dispatcher.stop_polling()
			else:
				await asyncio.sleep(5)
