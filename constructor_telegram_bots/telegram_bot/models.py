from django.db import models

# Create your models here.
class TelegramBotUserMessage(models.Model):
	message = models.TextField()
	date_sent = models.DateTimeField(auto_now_add=True)

class TelegramBotUser(models.Model):
	chat_id = models.IntegerField()
	username = models.CharField(max_length=32)
	telegram_bot_user_messages = models.ManyToManyField(TelegramBotUserMessage)
	date_started = models.DateTimeField(auto_now_add=True)

class TelegramBotCommand(models.Model):
	callback = models.CharField(max_length=64, null=True)
	command = models.CharField(max_length=32, null=True)
	is_edit_last_message = models.BooleanField()
	command_answer = models.TextField()
	keyboard = models.JSONField(null=True)

class TelegramBot(models.Model):
	name = models.CharField(max_length=32)
	token = models.CharField(max_length=50)
	private = models.BooleanField(default=True)
	telegram_bot_users = models.ManyToManyField(TelegramBotUser)
	telegram_bot_command = models.ManyToManyField(TelegramBotCommand)
	date_added = models.DateTimeField(auto_now_add=True)