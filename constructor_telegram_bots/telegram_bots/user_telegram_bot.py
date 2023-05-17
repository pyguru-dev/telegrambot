from aiogram.dispatcher import Dispatcher, FSMContext
from aiogram.types import Message, CallbackQuery, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram import Bot

from telegram_bot.models import TelegramBot, TelegramBotCommand, TelegramBotCommandManager, TelegramBotUser, TelegramBotUserManager

from asgiref.sync import sync_to_async
import aiohttp
import asyncio
import json


class UserTelegramBot:
	def __init__(self, telegram_bot: TelegramBot) -> None:
		self.telegram_bot = telegram_bot
		self.loop = asyncio.new_event_loop()

	async def message_and_callback_query_handler(*args, **kwargs) -> None:
		self: 'UserTelegramBot' = args[0]

		if isinstance(args[1], Message):
			message: Message = args[1]

			user_id: int = message.from_user.id
			username: str = message.from_user.username
		else:
			callback_query: CallbackQuery = args[1]
			message: Message = callback_query.message

			user_id: int = callback_query.from_user.id
			username: str = callback_query.from_user.username

		users: TelegramBotUserManager = await sync_to_async(TelegramBotUser.objects.filter)(user_id=user_id)
		if await users.aexists() is False:
			user: TelegramBotUser = await sync_to_async(TelegramBotUser.objects.add_telegram_bot_user)(
				telegram_bot=self.telegram_bot,
				user_id=user_id,
				username=username
			)
			await user.asave()
		else:
			user: TelegramBotUser = await users.aget()

		if self.telegram_bot.is_private and user.is_allowed or self.telegram_bot.is_private is False:
			if isinstance(args[1], Message):
				commands: TelegramBotCommandManager = await sync_to_async(self.telegram_bot.commands.filter)(command=message.text)
			else:
				commands: TelegramBotCommandManager = await sync_to_async(self.telegram_bot.commands.filter)(callback=callback_query.data)

			if await commands.aexists():
				command: TelegramBotCommand = await commands.aget()

				command_message_text = command.message_text
				command_message_text = command_message_text.replace('${user_id}', str(user_id))
				command_message_text = command_message_text.replace('${username}', username)

				if isinstance(args[1], Message):
					command_message_text = command_message_text.replace('${user_message_text}', message.text)

				if command_message_text.find('${web_api}:{') != -1:
					web_api_url = command_message_text.split('${web_api}:{')[1].split('}')[0]

					if web_api_url.find('http://') != -1 or web_api_url.find('https://') != -1:
						async with aiohttp.ClientSession() as session:
							async with session.get(web_api_url) as responce:
								if responce.status == 200:
									responce_text = await responce.text()
								else:
									responce_text = 'Web-API не найден!'
					else:
						responce_text = 'Ссылка на Web-API недействительна!'

					command_message_text = command_message_text.replace('${web_api}:{' + web_api_url + '}', responce_text)

				keyboard_buttons: list = json.loads(command.keyboard)
				keyboard_type: str = keyboard_buttons.pop(0)
				
				if keyboard_type == 'defaultKeyboard':
					keyboard = ReplyKeyboardMarkup(row_width=1, one_time_keyboard=True)
					
					for num in range(len(keyboard_buttons)):
						keyboard.add(
							KeyboardButton(text=keyboard_buttons[num])
						)
				elif keyboard_type == 'inlineKeyboard':
					keyboard = InlineKeyboardMarkup(row_width=1)

					for num in range(len(keyboard_buttons)):
						button: list = keyboard_buttons[num].split('}:{')
						button_text: str = button[0].replace('{', '')
						button_url_or_callback_data: str = button[1].replace('}', '')

						if button[1].find('http://') != -1 or button[1].find('https://') != -1:
							keyboard.add(
								InlineKeyboardButton(text=button_text, url=button_url_or_callback_data)
							)
						else:
							keyboard.add(
								InlineKeyboardButton(text=button_text, callback_data=button_url_or_callback_data)
							)
				else:
					keyboard = None

				chat_id: int = message.chat.id

				if len(command_message_text) > 4096:
					command_message_text = 'Слишком длинное сообщение!'

				if isinstance(args[1], Message):
					await self.dispatcher.bot.send_message(
						chat_id=chat_id,
						text=command_message_text,
						reply_markup=keyboard
					)
				else:
					await self.dispatcher.bot.edit_message_text(
						chat_id=chat_id,
						message_id=message.message_id,
						text=command_message_text,
						reply_markup=keyboard
					)

	async def setup(self) -> None:
		self.bot = Bot(token=self.telegram_bot.api_token, loop=self.loop)
		self.dispatcher = Dispatcher(bot=self.bot)

		self.dispatcher.register_message_handler(self.message_and_callback_query_handler)
		self.dispatcher.register_callback_query_handler(self.message_and_callback_query_handler)

	async def start(self) -> None:
		self.loop.create_task(self.stop())

		await self.dispatcher.skip_updates()
		await self.dispatcher.start_polling()

		session = await self.bot.get_session()
		await session.close()

		self.telegram_bot.is_stopped = True
		await self.telegram_bot.asave()

	async def stop(self) -> None:
		while self.telegram_bot.is_running:
			self.telegram_bot = await TelegramBot.objects.aget(id=self.telegram_bot.id)

			if self.telegram_bot.is_running is False:
				self.dispatcher.stop_polling()
			else:
				await asyncio.sleep(5)
