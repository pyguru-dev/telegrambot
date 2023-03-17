from django.db import models

from telegram_bot.managers import TelegramBotManager, TelegramBotCommandManager

class TelegramBotUserMessage(models.Model):
	message = models.TextField()
	date_sent = models.DateTimeField(auto_now_add=True)

class TelegramBotUser(models.Model):
	user_id = models.BigIntegerField()
	username = models.CharField(max_length=32)
	telegram_bot_user_messages = models.ManyToManyField(TelegramBotUserMessage)
	date_started = models.DateTimeField(auto_now_add=True)

class TelegramBotCommand(models.Model):
	name = models.CharField(max_length=255)
	command = models.CharField(max_length=32, null=True)
	callback = models.CharField(max_length=64, null=True)
	is_edit_last_message = models.BooleanField()
	message_text = models.TextField()
	keyboard = models.JSONField(null=True)

	objects = TelegramBotCommandManager()

class TelegramBot(models.Model):
	name = models.CharField(max_length=32)
	token = models.CharField(max_length=50, unique=True)
	private = models.BooleanField(default=True)
	is_running = models.BooleanField(default=False)
	commands = models.ManyToManyField(TelegramBotCommand)
	users = models.ManyToManyField(TelegramBotUser, related_name='users')
	allowed_users = models.ManyToManyField(TelegramBotUser, related_name='allowed_users')
	date_added = models.DateTimeField(auto_now_add=True)

	USERNAME_FIELD = 'id'
	REQUIRED_FIELDS = ['token', 'private']

	objects = TelegramBotManager()