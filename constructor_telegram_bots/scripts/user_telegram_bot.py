from aiogram.dispatcher import Dispatcher, FSMContext
from aiogram.types import Message, CallbackQuery, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram import Bot

from telegram_bot.models import TelegramBot

from asgiref.sync import sync_to_async
from typing import Union
import aiohttp
import asyncio
import json


class UserTelegramBot:
	def __init__(self, telegram_bot: TelegramBot) -> None:
		self.telegram_bot = telegram_bot
		self.loop = None

	async def setup(self) -> None:
		self.bot = Bot(token=self.telegram_bot.api_token, loop=self.loop)
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
				button: list = keyboard_buttons[num].split(':')
				button_text: str = button[0].replace('{', '')
				button_url_or_callback_data: str = button[1].replace('}', '')

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
	
	async def get_message_text_for_telegram_bot(self, user_id: int, username: str, message_text: str) -> str:
		message_text = message_text.replace('${user_id}', str(user_id))
		message_text = message_text.replace('${username}', username)

		if message_text.find('${web_api:') != -1:
			async with aiohttp.ClientSession() as session:
				web_api_url = message_text.split('${web_api:')[1].split('}')[0]
				async with session.get(web_api_url) as responce:
					responce_text = await responce.text()
			
			message_text = message_text.replace('${web_api:' + web_api_url + '}', responce_text)

		return message_text

	async def callback_query_handler(self, callback_query: CallbackQuery, state: FSMContext) -> None:
		async for telegram_bot_command in self.telegram_bot.commands.all():
			if telegram_bot_command.callback == callback_query.data:
				keyboard: dict = await self.get_keyboard_for_telegram_bot(telegram_bot_command.keyboard)
				message_text: str = await self.get_message_text_for_telegram_bot(callback_query.from_user.id, callback_query.from_user.username, telegram_bot_command.message_text)

				await  self.dispatcher.bot.edit_message_text(chat_id=state.chat, message_id=callback_query.message.message_id, text=message_text, **keyboard)

	async def message_handler(self, message: Message) -> None:
		async for telegram_bot_command in self.telegram_bot.commands.all():
			if telegram_bot_command.command == message.text:
				keyboard: dict = await self.get_keyboard_for_telegram_bot(telegram_bot_command.keyboard)
				message_text: str = await self.get_message_text_for_telegram_bot(message.from_user.id, message.from_user.username, telegram_bot_command.message_text)

				await self.dispatcher.bot.send_message(chat_id=message.chat.id, text=message_text, **keyboard)

	async def stop(self) -> None:
		while True:
			self.telegram_bot: TelegramBot = await sync_to_async(TelegramBot.objects.get)(id=self.telegram_bot.id)
			if self.telegram_bot.is_running:
				await asyncio.sleep(5)
			else:
				self.dispatcher.stop_polling()

				self.telegram_bot.is_stopped = True
				await sync_to_async(self.telegram_bot.save)()

				break

	async def start(self) -> None:
		self.loop.create_task(self.stop())

		await self.dispatcher.skip_updates()
		await self.dispatcher.start_polling()
