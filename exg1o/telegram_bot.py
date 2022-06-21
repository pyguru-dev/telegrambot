from konstruktor.models import TelegramBotLogModel, TelegramBotCommandModel
from telegram.ext import Updater, MessageHandler, CommandHandler, Filters
import telegram.ext
import telegram

class TelegramBot: # Telegram Бот
	def __init__(self, owner, bot_id, token):
		self.owner = owner
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
			_id, user_full_name, message = update.effective_chat.id, update.effective_user.full_name, update.message.text

			log = TelegramBotLogModel(id, self.bot_id, self.owner, user_full_name, message)
			log.save()

			func(self, update, context, _id, message)
		wrapper.__name__ = func.__name__
		return wrapper

	def send_message(func): # Отправка ответа пользователю на команду бота
		def wrapper(self, update: telegram.update.Update, context: telegram.ext.callbackcontext.CallbackContext, id: int, message: str):
			for bot_command in TelegramBotCommandModel.objects.filter(owner=self.owner).filter(bot_id=self.bot_id):
				if bot_command.command == message:
					command_answer = bot_command.command_answer
					for variable in ('{user_name}', '{user_surname}'):
						if command_answer.find(variable) != -1:
							command_answer = command_answer.split(variable)
							if variable == '{user_name}':
								command_answer = update.effective_user.first_name.join(command_answer)
							elif variable == '{user_surname}':
								command_answer = update.effective_user.last_name.join(command_answer)
					context.bot.send_message(chat_id=id, text=command_answer)

			func(self, update, context, id, message)
		wrapper.__name__ = func.__name__
		return wrapper

	@get_user_id_and_messaage
	@send_message
	def new_message(self, update: telegram.update.Update, context: telegram.ext.callbackcontext.CallbackContext, id: int, message: str): # Получение обычного сообщения
		pass

	@get_user_id_and_messaage
	@send_message
	def execute_command(self, update: telegram.update.Update, context: telegram.ext.callbackcontext.CallbackContext, id: int, message: str): # Получение командного сообщения
		pass

	def start(self): # Запуск бота
		new_message_handler = MessageHandler(Filters.text & (~Filters.command), self.new_message)
		self.dispatcher.add_handler(new_message_handler)

		for bot_command in TelegramBotCommandModel.objects.filter(owner=self.owner).filter(bot_id=self.bot_id):
			if list(bot_command.command)[0] == '/':
				handler = CommandHandler(''.join(list(bot_command.command)[1:len(bot_command.command)]), self.execute_command)
				self.dispatcher.add_handler(handler)

		self.updater.start_polling()

	def stop(self): # Остоновка бота
		self.updater.stop()