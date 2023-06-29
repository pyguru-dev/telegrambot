from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram import Bot

from telegram_bot.services.custom_aiogram import CustomDispatcher

from django.contrib.auth.models import UserManager
from django.conf import settings

from user.models import User

from asgiref.sync import sync_to_async
from asyncio.events import AbstractEventLoop
import asyncio

from functools import wraps


class ConstructorTelegramBot:
	def __init__(self) -> None:
		self.loop: AbstractEventLoop = asyncio.new_event_loop()

	def check_user(func):
		@wraps(func)
		async def wrapper(*args, **kwargs):
			message = args[1]

			user: UserManager = await sync_to_async(User.objects.filter)(id=message.from_user.id)
			if await user.aexists() is False:
				await sync_to_async(User.objects.create_user)(user_id=message.from_user.id)

			return await func(*args, **kwargs)
		return wrapper

	@check_user
	async def start_command(self, message: Message) -> None:
		await self.bot.send_message(
			chat_id=message.chat.id,
			text=f"""\
				Привет, @{message.from_user.username}!
				Я являюсь Telegram ботом для сайта Constructor Telegram Bots.
				Спасибо за то, что ты с нами ❤️
			""".replace('	', '')
		)
		
		message_list: list = message.text.split()
		if len(message_list) > 1:
			if message_list[1] == 'login':
				await self.login_command(message)

	@check_user
	async def login_command(self, message: Message) -> None:
		user: User = await User.objects.aget(id=message.from_user.id)
		login_url: str = await user.alogin_url

		inline_keyboard = InlineKeyboardMarkup(row_width=1)
		inline_keyboard.add(
			InlineKeyboardButton(text='Авторизация', url=login_url)
		)

		await self.bot.send_message(
			chat_id=message.chat.id,
			text='Нажмите на кнопку ниже, чтобы авторизоваться на сайте.',
			reply_markup=inline_keyboard
		)

	async def setup(self) -> None:
		self.bot = Bot(token=settings.CONSTRUCTOR_TELEGRAM_BOT_API_TOKEN, loop=self.loop)
		self.dispatcher = CustomDispatcher(bot_username=settings.CONSTRUCTOR_TELEGRAM_BOT_USERNAME, bot=self.bot)

		self.dispatcher.register_message_handler(self.start_command, commands=['start'])
		self.dispatcher.register_message_handler(self.login_command, commands=['login'])

	async def start(self) -> None:
		await self.dispatcher.skip_updates()
		await self.dispatcher.start_polling()
