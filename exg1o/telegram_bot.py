from konstruktor.models import TelegramBotModel, TelegramBotLogModel, TelegramBotCommandModel
import global_variable as GlobalVariable
from telegram.ext import Updater, MessageHandler, CommandHandler, Filters
from threading import Thread
import telegram.ext
import telegram
import time

class TelegramBot: # Telegram Бот
	def __init__(self, bot_id, token):
		self.bot_id = bot_id
		self.token = token

	def auth(self): # Авторизация бота в Telegram API
		try:
			self.updater = Updater(token=self.token)
			self.dispatcher = self.updater.dispatcher

			return True
		except telegram.error.InvalidToken:
			return False

	def get_user_id_and_messaage(func): # Получение ID пользователя и его сообщения
		def wrapper(self, update: telegram.update.Update, context: telegram.ext.callbackcontext.CallbackContext):
			chat_id, user_full_name, user_message = update.effective_chat.id, update.effective_user.full_name, update.message.text

			log = TelegramBotLogModel(None, self.bot_id, user_full_name, user_message)
			log.save()

			func(self, update, context, chat_id, user_message)
		wrapper.__name__ = func.__name__
		return wrapper

	def send_message(func): # Отправка ответа пользователю на команду бота
		def wrapper(self, update: telegram.update.Update, context: telegram.ext.callbackcontext.CallbackContext, chat_id: int, user_message: str):
			for bot_command in TelegramBotCommandModel.objects.filter(bot_id=self.bot_id):
				if bot_command.command == user_message:
					command_answer = bot_command.command_answer
					for variable_for_command in GlobalVariable.VARIABLES_FOR_COMMANDS:
						variable = variable_for_command['variable']
						if command_answer.find(variable) != -1:
							command_answer = command_answer.split(variable)
							command_answer = str(eval(variable_for_command[variable])).join(command_answer)
					context.bot.send_message(chat_id=chat_id, text=command_answer)

			func(self, update, context, chat_id, user_message)
		wrapper.__name__ = func.__name__
		return wrapper

	@get_user_id_and_messaage
	@send_message
	def new_message(self, update: telegram.update.Update, context: telegram.ext.callbackcontext.CallbackContext, chat_id: int, message: str): # Получение обычного сообщения
		pass

	@get_user_id_and_messaage
	@send_message
	def execute_command(self, update: telegram.update.Update, context: telegram.ext.callbackcontext.CallbackContext, chat_id: int, message: str): # Получение командного сообщения
		pass

	def start(self): # Запуск бота
		new_message_handler = MessageHandler(Filters.text & (~Filters.command), self.new_message)
		self.dispatcher.add_handler(new_message_handler)

		for bot_command in TelegramBotCommandModel.objects.filter(bot_id=self.bot_id):
			if list(bot_command.command)[0] == '/':
				handler = CommandHandler(''.join(list(bot_command.command)[1:len(bot_command.command)]), self.execute_command)
				self.dispatcher.add_handler(handler)

		self.updater.start_polling()
		Thread(target=self.stop, daemon=True).start()
	
	def stop(self): # Остоновка бота
		while True:
			self.bot = TelegramBotModel.objects.get(id=self.bot_id)
			if self.bot.online == False:
				self.updater.stop()
				break
			time.sleep(1)