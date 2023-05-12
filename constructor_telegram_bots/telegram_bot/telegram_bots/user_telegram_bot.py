from aiogram.dispatcher import Dispatcher, FSMContext
from aiogram.types import Message, CallbackQuery, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram import Bot

from telegram_bot.models import TelegramBot, TelegramBotCommandManager, TelegramBotUser, TelegramBotUserManager

from asgiref.sync import sync_to_async
from typing import Union
import aiohttp
import asyncio
import json


class UserTelegramBot:
	def __init__(self, telegram_bot: TelegramBot) -> None:
		self.telegram_bot = telegram_bot
		self.loop = None
	
	def get_message_text(func):
		async def wrapper(*args, **kwargs):
			message_text = kwargs['command'].message_text
			message_text = message_text.replace('${user_id}', str(kwargs['user_id']))
			message_text = message_text.replace('${username}', kwargs['username'])

			if message_text.find('${web_api}:{') != -1:
				async with aiohttp.ClientSession() as session:
					web_api_url = message_text.split('${web_api}:{')[1].split('}')[0]
					async with session.get(web_api_url) as responce:
						responce_text = await responce.text()
				
				message_text = message_text.replace('${web_api}:{' + web_api_url + '}', responce_text)

			kwargs.update({'message_text': message_text})

			return await func(*args, **kwargs)
		return wrapper
	
	def get_keyboard(func):
		async def wrapper(*args, **kwargs):
			keyboard_buttons: list = json.loads(kwargs['command'].keyboard)
			keyboard_type: str = keyboard_buttons.pop(0)
			
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

			del kwargs['command']
			kwargs.update({'keyboard': keyboard})

			return await func(*args, **kwargs)
		return wrapper
	
	@get_message_text
	@get_keyboard
	async def execute_command(
		self,
		chat_id: int,
		user_id: int,
		username: str,
		message_text: str,
		keyboard: Union[ReplyKeyboardMarkup, InlineKeyboardMarkup],
		*,
		message_id: int = None
	) -> None:
		users: TelegramBotUserManager = await sync_to_async(TelegramBotUser.objects.filter)(user_id=user_id)
		if await users.aexists() is False:
			user: TelegramBotUser = await sync_to_async(TelegramBotUser.objects.add_telegram_bot_user)(telegram_bot=self.telegram_bot, user_id=user_id, username=username)
			await user.asave()
		else:
			user: TelegramBotUser = await users.aget()

		if user.is_allowed and self.telegram_bot.is_private or self.telegram_bot.is_private is False:
			if message_id is None:
				await self.dispatcher.bot.send_message(chat_id=chat_id, text=message_text, **keyboard)
			else:
				await self.dispatcher.bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=message_text, **keyboard)

	async def callback_query_handler(self, callback_query: CallbackQuery, state: FSMContext) -> None:
		commands: TelegramBotCommandManager = await sync_to_async(self.telegram_bot.commands.filter)(callback=callback_query.data)
		if await commands.aexists():
			await self.execute_command(
				chat_id=state.chat,
				user_id=state.user,
				username=callback_query.from_user.username,
				command=await commands.aget(),
				message_id=callback_query.message.message_id
			)

	async def message_handler(self, message: Message) -> None:
		commands: TelegramBotCommandManager = await sync_to_async(self.telegram_bot.commands.filter)(command=message.text)
		if await commands.aexists():
			await self.execute_command(
				chat_id=message.chat.id,
				user_id=message.from_user.id,
				username=message.from_user.username,
				command=await commands.aget(),
			)

	async def setup(self) -> None:
		self.bot = Bot(token=self.telegram_bot.api_token, loop=self.loop)
		self.dispatcher = Dispatcher(bot=self.bot)

		self.dispatcher.register_message_handler(self.message_handler)
		self.dispatcher.register_callback_query_handler(self.callback_query_handler)

	async def start(self) -> None:
		self.loop.create_task(self.stop())

		await self.dispatcher.skip_updates()
		await self.dispatcher.start_polling()

	async def stop(self) -> None:
		while True:
			self.telegram_bot = await TelegramBot.objects.aget(id=self.telegram_bot.id)
			if self.telegram_bot.is_running:
				await asyncio.sleep(5)
			else:
				self.dispatcher.stop_polling()

				self.telegram_bot.is_stopped = True
				await self.telegram_bot.asave()

				break
