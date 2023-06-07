from aiogram import Bot, types
from telegram_bots.custom_aiogram import CustomDispatcher

from aiogram.utils.exceptions import ValidationError, Unauthorized
from django.core.exceptions import ObjectDoesNotExist

from telegram_bot.models import (
	TelegramBot,
	TelegramBotCommand, TelegramBotCommandManager,
	TelegramBotCommandKeyboard,
	TelegramBotUser, TelegramBotUserManager
)

from asgiref.sync import sync_to_async
import asyncio
import aiohttp

from typing import Union


class UserTelegramBot:
	def __init__(self, telegram_bot: TelegramBot) -> None:
		self.telegram_bot = telegram_bot
		self.loop = asyncio.new_event_loop()

	async def check_user(self, user_id: int, username: str) -> TelegramBotUser:
		users: TelegramBotUserManager = await sync_to_async(TelegramBotUser.objects.filter)(user_id=user_id)
		if await users.aexists() is False:
			user: TelegramBotUser = await sync_to_async(TelegramBotUser.objects.create)(
				telegram_bot=self.telegram_bot,
				user_id=user_id,
				username=username
			)
			await user.asave()
		else:
			user: TelegramBotUser = await users.aget()

		return user
	
	def get_command_keyboard(sefl, command) -> TelegramBotCommandKeyboard:
		try:
			return command.keyboard
		except ObjectDoesNotExist:
			return None
	
	def get_command_keyboard_button_command(sefl, button) -> TelegramBotCommand:
		return button.telegram_bot_command
	
	async def search_command(self, message_text: str = None, button_id: int = None):
		command = None

		async for command_ in self.telegram_bot.commands.all():
			if command is not None:
				break

			keyboard: TelegramBotCommandKeyboard = await sync_to_async(self.get_command_keyboard)(command_)

			if keyboard is not None:
				is_finded_keyboard = False

				if keyboard.type == 'default' and message_text is not None:
					is_finded_keyboard = True
				elif keyboard.type == 'inline' and button_id is not None:
					is_finded_keyboard = True

				if is_finded_keyboard:
					async for button in keyboard.buttons.all():
						is_finded_button = False

						if button.text == message_text and message_text is not None:
							is_finded_button = True
						if button.id == button_id and button_id is not None:
							is_finded_button = True

						if is_finded_button:
							command: TelegramBotCommand = await sync_to_async(self.get_command_keyboard_button_command)(button)
							break

		return command
	
	async def get_command(self, message_text: str = None, button_id: int = None) -> TelegramBotCommand:
		if message_text is not None:
			commands: TelegramBotCommandManager = await sync_to_async(self.telegram_bot.commands.filter)(command=message_text)

			if await commands.aexists():
				command: TelegramBotCommand = await commands.afirst()
			else:
				command: Union[TelegramBotCommand, None] = await self.search_command(message_text=message_text)
		else:
			command: Union[TelegramBotCommand, None] = await self.search_command(button_id=button_id)

		return command

	async def message_and_callback_query_handler(self, *args, **kwargs) -> None:
		if isinstance(args[0], types.Message):
			type = 'message'
		else:
			type = 'callback_query'
		
		if type == 'message':
			message: types.Message = args[0]

			user_id: int = message.from_user.id
			username: str = message.from_user.username
		else:
			callback_query: types.CallbackQuery = args[0]
			message: types.Message = callback_query.message

			user_id: int = callback_query.from_user.id
			username: str = callback_query.from_user.username

		user: TelegramBotUser = await self.check_user(user_id=user_id, username=username)

		if self.telegram_bot.is_private and user.is_allowed or self.telegram_bot.is_private is False:
			if type == 'message':
				command: TelegramBotCommand = await self.get_command(message_text=message.text)
			else:
				command: TelegramBotCommand = await self.get_command(button_id=int(callback_query.data))

			if command is not None:
				if command.api_request is not None:
					try:
						async with aiohttp.ClientSession() as session:
							async with session.post(url=command.api_request['url'], data=command.api_request['data']) as response:
								pass
					except aiohttp.client_exceptions.InvalidURL:
						pass

				keyboard: TelegramBotCommandKeyboard = await sync_to_async(self.get_command_keyboard)(command)
				
				if keyboard is not None:
					if keyboard.type == 'default':
						tg_keyboard = types.ReplyKeyboardMarkup()
						
						async for button in keyboard.buttons.all():
							tg_keyboard.add(
								types.KeyboardButton(text=button.text)
							)
					else:
						tg_keyboard = types.InlineKeyboardMarkup()

						async for button in keyboard.buttons.all():
							tg_keyboard.add(
								types.InlineKeyboardButton(text=button.text, callback_data=button.id)
							)
				else:
					tg_keyboard = None

				if type == 'callback_query':
					await self.dispatcher.bot.delete_message(
						chat_id=message.chat.id,
						message_id=message.message_id
					)

				if command.image == '':
					await self.dispatcher.bot.send_message(
						chat_id=message.chat.id,
						text=command.message_text,
						reply_markup=tg_keyboard
					)
				else:
					await self.dispatcher.bot.send_photo(
						chat_id=message.chat.id,
						photo=types.InputFile(command.image.path),
						caption=command.message_text,
						reply_markup=tg_keyboard
					)

	async def setup(self) -> None:
		self.bot = Bot(token=self.telegram_bot.api_token, loop=self.loop)
		self.dispatcher = CustomDispatcher(bot=self.bot)

		self.dispatcher.register_message_handler(self.message_and_callback_query_handler)
		self.dispatcher.register_callback_query_handler(self.message_and_callback_query_handler)

	async def start(self) -> None:
		try:
			task = self.loop.create_task(self.stop())

			await self.dispatcher.skip_updates()
			await self.dispatcher.start_polling()

			task.cancel()

			session = await self.bot.get_session()
			await session.close()

			self.telegram_bot.is_stopped = True
			await self.telegram_bot.asave()
		except (ValidationError, Unauthorized):
			task.cancel()

			session = await self.bot.get_session()
			await session.close()

			await self.telegram_bot.adelete()

	async def stop(self) -> None:
		while self.telegram_bot.is_running:
			self.telegram_bot = await TelegramBot.objects.aget(id=self.telegram_bot.id)

			if self.telegram_bot.is_running is False:
				self.dispatcher.stop_polling()
			else:
				await asyncio.sleep(5)
