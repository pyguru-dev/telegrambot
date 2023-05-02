from telegram.ext import Updater, CommandHandler
from telegram.ext.callbackcontext import CallbackContext
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.update import Update

from django.conf import settings

from user.models import User

from scripts.decorators import TelegramBotDecorators


class ConstructorTelegramBot:
	def __init__(self) -> None:
		self.commands = {
			'start': self.start_command,
			'auth': self.auth_command,
			'support': self.support_command,
		}

	@TelegramBotDecorators.get_attributes(need_attributes=('update', 'context', 'user_id', 'username', 'message',))
	def start_command(self, update: Update, context: CallbackContext, user_id: int, username: str, message: str) -> None:
		if User.objects.filter(id=user_id).exists() is False:
			User.objects.create_user(user_id=user_id)
			
			context.bot.send_message(
				chat_id=user_id,
			    text=f"""\
					Привет, @{username}!
					Я являюсь Telegram ботом для сайта Constructor Telegram Bots.
					Спасибо за то, что ты с нами ❤️
				""".replace('	', ''),
				reply_markup=InlineKeyboardMarkup(
					[
						[
							InlineKeyboardButton(text='Constructor Telegram Bots', url=settings.SITE_DOMAIN),
						],
					]
				)
			)
		
		if len(message.split()) > 1:
			if message.split()[1] == 'auth':
				self.auth_command(update, context)

	@TelegramBotDecorators.get_attributes(need_attributes=('context', 'user_id',))
	def auth_command(self, context: CallbackContext, user_id: int) -> None:
		context.bot.send_message(
			chat_id=user_id,
			text='Нажмите на кнопку ниже, чтобы авторизоваться на сайте.',
			reply_markup=InlineKeyboardMarkup(
				[
					[
						InlineKeyboardButton(text='Авторизация', url=User.objects.get(id=user_id).get_auth_url()),
					],
				]
			)
		)

	@TelegramBotDecorators.get_attributes(need_attributes=('context', 'user_id',))
	def support_command(self, context: CallbackContext, user_id: int) -> None:
		context.bot.send_message(
			chat_id=user_id,
			text='Нажмите на кнопку ниже, чтобы написать автору сайта.',
			reply_markup=InlineKeyboardMarkup(
				[
					[
						InlineKeyboardButton(text='Написать автору сайта', url='https://t.me/pycoder39'),
					],
				]
			)
		)

	def start(self) -> None:
		self.updater = Updater(token=settings.API_TOKEN)
		self.dispatcher = self.updater.dispatcher

		for command in self.commands:
			handler = CommandHandler(command, self.commands[command])
			self.dispatcher.add_handler(handler)

		self.updater.start_polling()
