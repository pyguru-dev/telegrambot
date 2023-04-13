from telegram.ext import Updater, Dispatcher, MessageHandler, Filters, CallbackQueryHandler
from telegram.ext.callbackcontext import CallbackContext
from telegram import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.update import Update

from telegram_bot.models import TelegramBot, TelegramBotCommand

from scripts.decorators import TelegramBotDecorators

from threading import Thread
import json
import time

class UserTelegramBot:
	def __init__(self, telegram_bot: TelegramBot) -> None:
		self.telegram_bot = telegram_bot

	def execute_command(self, update: Update, context: CallbackContext, telegram_bot_command: TelegramBotCommand) -> None:
		keyboard: list = json.loads(telegram_bot_command.keyboard)
		keyboard_type: str = keyboard[0]

		del keyboard[0]
		
		if keyboard_type == 'defaultKeyboard':
			buttons = []
			for num in range(len(keyboard)):
				buttons.append(
					[
						KeyboardButton(text=keyboard[num]),
					]
				)

			keyboard = ReplyKeyboardMarkup(buttons)
		elif keyboard_type == 'inlineKeyboard':
			buttons = []
			for num in range(len(keyboard)):
				button: list = keyboard[num].split('}:{')
				button_text: str = button[0].replace('{', '')

				if button[1].find('http://') != -1 or button[1].find('https://') != -1:
					buttons.append(
						[
							InlineKeyboardButton(text=button_text, url=button[1].replace('}', '')),
						]
					)
				else:
					buttons.append(
						[
							InlineKeyboardButton(text=button_text, callback_data=button[1].replace('}', '')),
						]
					)

			keyboard = InlineKeyboardMarkup(buttons)

		variables = {
			'${user_id}':  str(update.effective_user.id),
			'${username}': update.effective_user.username,
			'${account_url}': update.effective_user.link,
			'${user_message}': update.effective_message.text,
		}

		message_text = telegram_bot_command.message_text
		for variable in variables:
			message_text = message_text.replace(variable, variables[variable])

		if keyboard_type == 'offKeyboard':
			context.bot.send_message(chat_id=update.effective_user.id, text=message_text)
		else:
			context.bot.send_message(chat_id=update.effective_user.id, text=message_text, reply_markup=keyboard)

	@TelegramBotDecorators.get_attributes(need_attributes=('update', 'context', 'callback_data',))
	@TelegramBotDecorators.check_telegram_bot_user
	def callback_query_handler(self, update: Update, context: CallbackContext, callback_data: str) -> None:
		for telegram_bot_command in self.telegram_bot.commands.all():
			if telegram_bot_command.callback == callback_data:
				self.execute_command(update, context, telegram_bot_command)

	@TelegramBotDecorators.get_attributes(need_attributes=('update', 'context', 'message',))
	@TelegramBotDecorators.check_telegram_bot_user
	def message_handler(self, update: Update, context: CallbackContext, message: str) -> None:
		for telegram_bot_command in self.telegram_bot.commands.all():
			if telegram_bot_command.command == message:
				self.execute_command(update, context, telegram_bot_command)

	def start(self) -> None:
		self.updater = Updater(token=self.telegram_bot.token)
		self.dispatcher = self.updater.dispatcher

		self.dispatcher.add_handler(CallbackQueryHandler(self.callback_query_handler))
		self.dispatcher.add_handler(MessageHandler(Filters.text, self.message_handler))
		self.dispatcher.add_handler(MessageHandler(Filters.command, self.message_handler))

		Thread(target=self.updater.start_polling, daemon=True).start()

		self.stop()

	def stop(self) -> None:
		while True:
			if TelegramBot.objects.get(id=self.telegram_bot.id).is_running:
				time.sleep(1)
			else:
				self.updater.stop()

				self.telegram_bot.is_stopped = True
				self.telegram_bot.save()

				break
