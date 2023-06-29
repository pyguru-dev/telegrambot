from aiogram import types
from aiogram.utils.exceptions import ValidationError, Unauthorized

from telegram_bot.services.custom_aiogram import CustomBot, CustomDispatcher

from telegram_bot.models import TelegramBot, TelegramBotCommand

from telegram_bot.services.user_telegram_bot import decorators, functions

import asyncio

from typing import Union


class TelegramBot:
	def __init__(self, telegram_bot: TelegramBot) -> None:
		self.loop = asyncio.new_event_loop()
		self.telegram_bot = telegram_bot

	@decorators.check_request
	@decorators.check_telegram_bot_user
	@decorators.check_telegram_bot_command
	@decorators.check_message_text
	async def message_and_callback_query_handler(
		self,
		message: types.Message,
		callback_query: Union[types.CallbackQuery, None],
		telegram_bot_command: TelegramBotCommand,
		message_text: str
	) -> None:
		telegram_keyboard: Union[types.ReplyKeyboardMarkup, types.InlineKeyboardMarkup] = await functions.get_telegram_keyboard(telegram_bot_command)

		if callback_query:
			await self.dispatcher.bot.delete_message(
				chat_id=message.chat.id,
				message_id=message.message_id
			)

		if not telegram_bot_command.image:
			await self.dispatcher.bot.send_message(
				chat_id=message.chat.id,
				text=message_text,
				reply_markup=telegram_keyboard
			)
		else:
			await self.dispatcher.bot.send_photo(
				chat_id=message.chat.id,
				photo=types.InputFile(telegram_bot_command.image.path),
				caption=message_text,
				reply_markup=telegram_keyboard
			)

	async def setup(self) -> None:
		self.bot = CustomBot(token=self.telegram_bot.api_token, loop=self.loop)
		self.dispatcher = CustomDispatcher(bot_username=self.telegram_bot.username, bot=self.bot)

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
