from telegram.ext import Updater, MessageHandler, CommandHandler, Filters, CallbackQueryHandler
from telegram.ext.callbackcontext import CallbackContext
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.update import Update

from user.models import User

import scripts.functions as Functions

class Decorators:
	def get_attributes(need_attributes: tuple):
		def decorator(func):
			def wrapper(*args, **kwargs):
				update: Update = args[1]

				attributes = {
					'update': update,
					'context': args[2],
				}

				if update.callback_query != None:
					attributes.update(
						{
							'callback_data': update.callback_query.data,
						}
					)
				if update.effective_user != None:
					attributes.update(
						{
							'user_id': update.effective_user.id,
							'username': update.effective_user.username,
						}
					)
				if update.effective_chat != None:
					attributes.update(
						{
							'chat_id': update.effective_chat.id,
						}
					)
				if update.effective_message != None:
					attributes.update(
						{
							'message': update.effective_message.text,
						}
					)

				kwargs = {}
				for attribute in attributes:
					for need_attribute in need_attributes:
						if attribute == need_attribute:
							kwargs.update(
								{
									attribute: attributes[attribute],
								}
							)

				if tuple(kwargs.keys()) == need_attributes:
					kwargs.update(
						{
							'self': args[0],
						}
					)

					return func(**kwargs)
				else:
					return Exception('Func attributes != need attributes!')
			return wrapper
		return decorator

class ConstructorTelegramBot:
	def __init__(self) -> None:
		self.commands = {
			'start': self.start_command,
			'auth': self.auth_command,
		}
		# self.callback = {
		# 	'test': self.test,
		# }

	# @Decorators.get_attributes(need_attributes=('update', 'context', 'callback_data',))
	# def handle_callback_query(self, update: Update, context: CallbackContext, callback_data: str) -> None:
	# 	callback_data: str = callback_data.split(':')[0]
	# 	if callback_data in self.callback:
	# 		self.callback[callback_data](update, context)
	
	# @Decorators.get_attributes(need_attributes=('message',))
	# def new_message(self, message: str) -> None:
	# 	print(message)

	@Decorators.get_attributes(need_attributes=('update', 'context', 'user_id', 'username', 'message',))
	def start_command(self, update: Update, context: CallbackContext, user_id: int, username: str, message: str) -> None:
		if len(message.split()) > 1:
			if message.split()[1] == 'auth':
				self.auth_command(update, context)

	@Decorators.get_attributes(need_attributes=('update', 'context', 'user_id', 'username', 'message',))
	def auth_command(self, update: Update, context: CallbackContext, user_id: int, username: str, message: str) -> None:
		if User.objects.filter(id=user_id).exists() == False:
			password = Functions.generator_secret_string(length=50, chars='abcdefghijklnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890')
			user = User(id=user_id, username=username, password=password)
			user.save()

		user = User.objects.get(id=user_id)
		keyboard = InlineKeyboardMarkup(
			[
				[
					InlineKeyboardButton(text='Авторизация', url=f'http://127.0.0.1:8000/user/auth/{user_id}/{user.password}/'),
				],
			]
		)

		context.bot.send_message(chat_id=user_id, text='Нажмите на кнопку ниже, чтобы авторизоваться на сайте.', reply_markup=keyboard)

	def start(self) -> None:
		with open('./data/constructor_telegram_bot.token', 'r') as constructor_telegram_bot_token_file:
			constructor_telegram_bot_token = constructor_telegram_bot_token_file.read()

		self.updater = Updater(token=constructor_telegram_bot_token)
		self.dispatcher = self.updater.dispatcher

		# self.dispatcher.add_handler(CallbackQueryHandler(self.handle_callback_query))

		# new_message_handler = MessageHandler(Filters.text & (~Filters.command), self.new_message)
		# self.dispatcher.add_handler(new_message_handler)

		for command in self.commands:
			handler = CommandHandler(command, self.commands[command])
			self.dispatcher.add_handler(handler)

		self.updater.start_polling()

	def stop(self) -> None:
		self.updater.stop()