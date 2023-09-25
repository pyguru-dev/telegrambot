from aiogram import types
from aiogram.utils.exceptions import *

from telegram_bot.services.custom_aiogram import CustomBot, CustomDispatcher

from telegram_bot.models import *

from .decorators import *
from .functions import get_keyboard

import asyncio
from aiohttp import ClientSession
from typing import Union


class UserTelegramBot:
	def __init__(self, telegram_bot: TelegramBot) -> None:
		self.telegram_bot = telegram_bot
		self.loop = asyncio.new_event_loop()

		self.bot = CustomBot(token=self.telegram_bot.api_token, loop=self.loop)
		self.dispatcher = CustomDispatcher(bot_username=self.telegram_bot.username, bot=self.bot)

	@check_telegram_bot_user
	@check_telegram_bot_command
	@check_telegram_bot_command_database_record
	@check_message_text
	async def message_and_callback_query_handler(
		self,
		request: Union[types.Message, types.CallbackQuery],
		telegram_bot_command: TelegramBotCommand,
		message_text: str
	) -> None:
		chat_id = (request if isinstance(request, types.Message) else request.message).chat.id
		telegram_bot_command_message_text: Optional[TelegramBotCommandMessageText] = await telegram_bot_command.aget_message_text()
		parse_mode = telegram_bot_command_message_text.mode if telegram_bot_command_message_text.mode != 'default' else None
		telegram_keyboard: Union[types.ReplyKeyboardMarkup, types.InlineKeyboardMarkup] = await get_keyboard(telegram_bot_command)

		async def send_answer(message_text: str):
			try:
				if isinstance(request, types.CallbackQuery):
					try:
						await self.dispatcher.bot.delete_message(
							chat_id=chat_id,
							message_id=request.message.message_id
						)
					except (MessageToDeleteNotFound, MessageCantBeDeleted):
						pass

				if telegram_bot_command.image:
					try:
						await self.dispatcher.bot.send_photo(
							chat_id=chat_id,
							photo=types.InputFile(telegram_bot_command.image.path),
							caption=message_text,
							parse_mode=parse_mode,
							reply_markup=telegram_keyboard
						)
						return
					except FileNotFoundError:
						telegram_bot_command.image = None
						await telegram_bot_command.asave()

				await self.dispatcher.bot.send_message(
					chat_id=chat_id,
					text=message_text,
					parse_mode=parse_mode,
					reply_markup=telegram_keyboard
				)
			except RetryAfter as exception:
				await asyncio.sleep(exception.timeout)
				await send_answer(message_text=message_text)

		await send_answer(message_text=message_text)

	async def setup(self) -> None:
		bot_commands = []

		async for telegram_bot_command in self.telegram_bot.commands.all():
			telegram_bot_command_command: TelegramBotCommandCommand = await telegram_bot_command.aget_command()

			if telegram_bot_command_command and telegram_bot_command_command.is_show_in_menu:
				bot_commands.append(types.BotCommand(
					command=telegram_bot_command_command.text.replace('/', ''),
					description=telegram_bot_command_command.description
				))

		await self.bot.set_my_commands(bot_commands)

		self.dispatcher.register_message_handler(self.message_and_callback_query_handler)
		self.dispatcher.register_callback_query_handler(self.message_and_callback_query_handler)

	async def start(self) -> None:
		task: asyncio.Task = self.loop.create_task(self.stop())

		try:
			await self.dispatcher.start_polling()

			self.telegram_bot.is_stopped = True
			await self.telegram_bot.asave()
		except (ValidationError, Unauthorized):
			await self.telegram_bot.adelete()

		task.cancel()

		session: ClientSession = await self.bot.get_session()
		await session.close()

	async def stop(self) -> None:
		while True:
			await self.telegram_bot.arefresh_from_db()

			if not self.telegram_bot.is_running:
				self.dispatcher.stop_polling()
				break

			await asyncio.sleep(5)
