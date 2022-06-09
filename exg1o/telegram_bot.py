from konstruktor.models import TelegramBotCommandModel
from telegram.ext import Updater, MessageHandler, CommandHandler, Filters
import telegram.ext
import telegram

class TelegramBot: # Telegram Бот
	def __init__(self, owner, bot_name, token):
		self.owner = owner
		self.bot_name = bot_name
		self.token = token

	def auth(self):
		try:
			self.updater = Updater(token=self.token)
			self.dispatcher = self.updater.dispatcher
			return True
		except telegram.error.InvalidToken:
			return False

	def get_user_id_and_messaage(func):
		def wrapper(self, update: telegram.update.Update, context: telegram.ext.callbackcontext.CallbackContext):
			id, message = update.effective_chat.id, update.message.text

			func(self, update, context, id, message)
		wrapper.__name__ = func.__name__
		return wrapper

	@get_user_id_and_messaage
	def new_message(self, update: telegram.update.Update, context: telegram.ext.callbackcontext.CallbackContext, id: int, message: str):
		for bot_command in TelegramBotCommandModel.objects.filter(owner=self.owner).filter(bot_name=self.bot_name):
			if bot_command.command == message:
				context.bot.send_message(chat_id=id, text=bot_command.command_answer)

	@get_user_id_and_messaage
	def execute_command(self, update: telegram.update.Update, context: telegram.ext.callbackcontext.CallbackContext, id: int, message: str):
		for bot_command in TelegramBotCommandModel.objects.filter(owner=self.owner).filter(bot_name=self.bot_name):
			if bot_command.command == message:
				context.bot.send_message(chat_id=id, text=bot_command.command_answer)

	def start(self):
		new_message_handler = MessageHandler(Filters.text & (~Filters.command), self.new_message)
		self.dispatcher.add_handler(new_message_handler)

		for bot_command in TelegramBotCommandModel.objects.filter(owner=self.owner).filter(bot_name=self.bot_name):
			if list(bot_command.command)[0] == '/':
				handler = CommandHandler(''.join(list(bot_command.command)[1:len(bot_command.command)]), self.execute_command)
				self.dispatcher.add_handler(handler)

		self.updater.start_polling()

if __name__ == '__main__': # Тест для бота
	bot = TelegramBot('Exg1o', 'Exg1oBot', '5573899324:AAF0DUX_sYa25-KTLTqrZBY7IvBXJSazYKA')
	if bot.auth():
		bot.start()
	else:
		print('Неверный "Token" бота!')