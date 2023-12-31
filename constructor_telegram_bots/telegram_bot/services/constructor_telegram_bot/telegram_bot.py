from telegram_bot.services.custom_aiogram import CustomBot, CustomDispatcher
from aiogram import types

from .decorators import *

from user.models import User

from django.conf import settings
import asyncio


class ConstructorTelegramBot:
	def __init__(self) -> None:
		self.loop: asyncio.AbstractEventLoop = asyncio.new_event_loop()

		self.bot = CustomBot(token=settings.CONSTRUCTOR_TELEGRAM_BOT_API_TOKEN, loop=self.loop)
		self.dispatcher = CustomDispatcher(bot_username=settings.CONSTRUCTOR_TELEGRAM_BOT_USERNAME, bot=self.bot)

	@check_user
	async def start_command(self, message: types.Message) -> None:
		await self.bot.send_message(chat_id=message.chat.id, text=f"""\
			Hello, @{message.from_user.username}!
			I am a Telegram bot for Constructor Telegram Bots site.
			Thank you for being with us ❤️
		""".replace('\t', ''))

		commands_list: list = message.text.split()

		if len(commands_list) > 1 and commands_list[1] == 'login':
			await self.login_command(message)

	@check_user
	async def login_command(self, message: types.Message) -> None:
		user: User = await User.objects.aget(telegram_id=message.from_user.id)

		keyboard = types.InlineKeyboardMarkup(row_width=1)
		keyboard.add(types.InlineKeyboardButton(text='Login', url=await user.alogin_url))

		await self.bot.send_message(chat_id=message.chat.id, text='Click on the button below to login on the site.', reply_markup=keyboard)

	async def setup(self) -> None:
		self.dispatcher.register_message_handler(self.start_command, commands=['start'])
		self.dispatcher.register_message_handler(self.login_command, commands=['login'])

	async def start(self) -> None:
		await self.dispatcher.skip_updates()
		await self.dispatcher.start_polling()
