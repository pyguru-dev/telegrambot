from aiogram.dispatcher import Dispatcher
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram import Bot

from django.conf import settings

from user.models import User

from asgiref.sync import sync_to_async
import asyncio


loop = asyncio.get_event_loop()


bot = Bot(token=settings.API_TOKEN, loop=loop)
dispatcher = Dispatcher(bot=bot)


@dispatcher.message_handler(commands=['start'])
async def start_command(message: Message) -> None:
	await bot.send_message(
		chat_id=message.chat.id,
		text=f"""\
			Привет, @{message.from_user.username}!
			Я являюсь Telegram ботом для сайта Constructor Telegram Bots.
			Спасибо за то, что ты с нами ❤️
		""".replace('	', '')
	)

@dispatcher.message_handler(commands=['auth'])
async def auth_command(message: Message) -> None:
	user: User = await sync_to_async(User.objects.get)(id=message.from_user.id)
	auth_url: str = await sync_to_async(user.get_auth_url)()

	inline_keyboard = InlineKeyboardMarkup(row_width=1)
	inline_keyboard.add(
		InlineKeyboardButton(text='Авторизация', url=auth_url)
	)

	await bot.send_message(
		chat_id=message.chat.id,
		text='Нажмите на кнопку ниже, чтобы авторизоваться на сайте.',
		reply_markup=inline_keyboard
	)

async def start() -> None:
	await dispatcher.skip_updates()
	await dispatcher.start_polling()
