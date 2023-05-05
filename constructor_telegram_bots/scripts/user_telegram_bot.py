from aiogram.dispatcher import Dispatcher, FSMContext
from aiogram.types import Message, CallbackQuery, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram import Bot

from telegram_bot.models import TelegramBot

from asgiref.sync import sync_to_async
from typing import Union
import asyncio
import json


class UserTelegramBot:
	def __init__(self, telegram_bot: TelegramBot) -> None:
		self.telegram_bot = telegram_bot

		self.loop = asyncio.get_event_loop()
		self.bot = Bot(token=self.telegram_bot.token, loop=self.loop)
		self.dispatcher = Dispatcher(bot=self.bot)

		self.dispatcher.register_message_handler(self.message_handler)
		self.dispatcher.register_callback_query_handler(self.callback_query_handler)

	async def get_keyboard_for_telegram_bot(self, telegram_bot_command_keyboard: str) -> Union[ReplyKeyboardMarkup, InlineKeyboardMarkup]:
		keyboard_buttons: list = json.loads(telegram_bot_command_keyboard)
		keyboard_type: str = keyboard_buttons[0]

		del keyboard_buttons[0]
		
		keyboard = {}
		if keyboard_type == 'defaultKeyboard':
			keyboard = {'reply_markup': ReplyKeyboardMarkup(row_width=1)}
			for num in range(len(keyboard_buttons)):
				keyboard['reply_markup'].add(
					KeyboardButton(text=keyboard_buttons[num])
				)
		elif keyboard_type == 'inlineKeyboard':
			for num in range(len(keyboard_buttons)):
				button: list = keyboard_buttons[num].split('}:{')
				button_text: str = button[0][1:len(button[0])]
				button_url_or_callback_data: str = button[1][0:-1]

				keyboard = {'reply_markup': InlineKeyboardMarkup(row_width=1)}
				if button[1].find('http://') != -1 or button[1].find('https://') != -1:
					keyboard['reply_markup'].add(
						InlineKeyboardButton(text=button_text, url=button_url_or_callback_data)
					)
				else:
					keyboard['reply_markup'].add(
						InlineKeyboardButton(text=button_text, callback_data=button_url_or_callback_data)
					)

		return keyboard

	async def callback_query_handler(self, callback_query: CallbackQuery, state: FSMContext) -> None:
		async for telegram_bot_command in self.telegram_bot.commands.all():
			if telegram_bot_command.callback == callback_query.data:
				keyboard = await self.get_keyboard_for_telegram_bot(telegram_bot_command.keyboard)

				await  self.dispatcher.bot.send_message(
					chat_id=state.chat.id,
					text=telegram_bot_command.message_text.replace('${user_id}', str(callback_query.from_user.id)).replace('${username}', callback_query.from_user.username),
					**keyboard
				)

	async def message_handler(self, message: Message) -> None:
		async for telegram_bot_command in self.telegram_bot.commands.all():
			if telegram_bot_command.command == message.text:
				keyboard = await self.get_keyboard_for_telegram_bot(telegram_bot_command.keyboard)

				await self.dispatcher.bot.send_message(
					chat_id=message.chat.id,
					text=telegram_bot_command.message_text.replace('${user_id}', str(message.from_user.id)).replace('${username}', message.from_user.username),
					**keyboard
				)

	async def stop(self) -> None:
		while True:
			self.telegram_bot = await sync_to_async(TelegramBot.objects.get)(id=self.telegram_bot.id)
			if self.telegram_bot.is_running:
				await asyncio.sleep(5)
			else:
				self.dispatcher.stop_polling()

				self.telegram_bot.is_stopped = True
				self.telegram_bot.save()
				
				self.loop.close()
				# break

	async def start(self) -> None:
		self.loop.create_task(self.stop())

		await self.dispatcher.skip_updates()
		await self.dispatcher.start_polling()
