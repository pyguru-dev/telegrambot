from aiogram.dispatcher import Dispatcher
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram import Bot

from django.contrib.auth.models import UserManager
from django.conf import settings

from user.models import User

from asgiref.sync import sync_to_async


class ConstructorTelegramBot:
	def __init__(self) -> None:
		self.loop = None

	async def setup(self) -> None:
		self.bot = Bot(token=settings.CONSTRUCTOR_TELEGRAM_BOT_API_TOKEN, loop=self.loop)
		self.dispatcher = Dispatcher(bot=self.bot)

		self.dispatcher.register_message_handler(self.start_command, commands=['start'])
		self.dispatcher.register_message_handler(self.login_command, commands=['login'])

	async def start_command(self, message: Message) -> None:
		await self.bot.send_message(
			chat_id=message.chat.id,
			text=f"""\
				Привет, @{message.from_user.username}!
				Я являюсь Telegram ботом для сайта Constructor Telegram Bots.
				Спасибо за то, что ты с нами ❤️
			""".replace('	', '')
		)

		user: UserManager = await sync_to_async(User.objects.filter)(id=message.from_user.id)
		user_exists: bool = await sync_to_async(user.exists)()
		
		if user_exists is False:
			await sync_to_async(User.objects.create_user)(user_id=message.from_user.id)
		
		message_list = message.text.split()
		if len(message_list) > 1:
			if message_list[1] == 'login':
				await self.login_command(message)

	async def login_command(self, message: Message) -> None:
		user: User = await sync_to_async(User.objects.get)(id=message.from_user.id)
		login_url: str = await sync_to_async(user.get_login_url)()

		inline_keyboard = InlineKeyboardMarkup(row_width=1)
		inline_keyboard.add(
			InlineKeyboardButton(text='Авторизация', url=login_url)
		)

		await self.bot.send_message(
			chat_id=message.chat.id,
			text='Нажмите на кнопку ниже, чтобы авторизоваться на сайте.',
			reply_markup=inline_keyboard
		)

	async def start(self) -> None:
		await self.dispatcher.skip_updates()
		await self.dispatcher.start_polling()
