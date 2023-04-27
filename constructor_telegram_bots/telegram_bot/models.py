from django.core.handlers.wsgi import WSGIRequest
from django.db import models

from telegram_bot.managers import TelegramBotManager, TelegramBotCommandManager

class TelegramBotLog(models.Model):
	level = models.CharField(max_length=7)
	message = models.TextField()
	date_added = models.DateTimeField(auto_now_add=True)

	class Meta:
		db_table = 'telegram_bot_log'

	def __str__(self) -> str:
		return f'[{self.date_added}]: {self.level} > {self.message}'

class TelegramBotUser(models.Model):
	user_id = models.BigIntegerField()
	username = models.CharField(max_length=32)
	date_started = models.DateTimeField(auto_now_add=True)

	class Meta:
		db_table = 'telegram_bot_user'

	def __str__(self) -> str:
		return f'{self.user_id} - @{self.username}'

class TelegramBotCommand(models.Model):
	name = models.CharField(max_length=255)
	command = models.CharField(max_length=32, null=True)
	callback = models.CharField(max_length=64, null=True)
	message_text = models.TextField()
	keyboard = models.JSONField(null=True)

	objects = TelegramBotCommandManager()

	class Meta:
		db_table = 'telegram_bot_command'

	def __str__(self) -> str:
		return self.name

class TelegramBot(models.Model):
	name = models.CharField(max_length=32)
	token = models.CharField(max_length=50, unique=True)
	private = models.BooleanField(default=True)
	is_running = models.BooleanField(default=False)
	is_stopped = models.BooleanField(default=True)
	commands = models.ManyToManyField(TelegramBotCommand, related_name='commands')
	users = models.ManyToManyField(TelegramBotUser, related_name='users')
	allowed_users = models.ManyToManyField(TelegramBotUser, related_name='allowed_users')
	logs = models.ManyToManyField(TelegramBotLog, related_name='telegram_bot_logs')
	date_added = models.DateTimeField(auto_now_add=True)

	objects = TelegramBotManager()

	class Meta:
		db_table = 'telegram_bot'

	def duplicate(self, request: WSGIRequest, token: str, private: bool):
		duplicated_telegram_bot: TelegramBot = TelegramBot.objects.add_telegram_bot(request=request, token=token, private=private)

		for telegram_bot_command in self.commands.all():
			TelegramBotCommand.objects.add_telegram_bot_command(
				telegram_bot=duplicated_telegram_bot,
				name=telegram_bot_command.name,
				command=telegram_bot_command.command,
				callback=telegram_bot_command.callback,
				message_text=telegram_bot_command.message_text,
				keyboard=telegram_bot_command.keyboard
			)

	def custom_delete(self) -> None:
		for telegram_bot_command in self.commands.all():
			telegram_bot_command.delete()

		for telegram_bot_user in self.users.all():
			telegram_bot_user.delete()

		self.delete()

	def __str__(self) -> str:
		return self.name
