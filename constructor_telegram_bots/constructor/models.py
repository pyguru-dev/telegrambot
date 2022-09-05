from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class TelegramBotModel(models.Model):
	owner = models.ForeignKey(User, on_delete=models.CASCADE)
	name = models.CharField(max_length=256)
	token = models.CharField(max_length=256)
	online = models.BooleanField(default=False)

	class Meta:
		verbose_name = 'Telegram Bot'
		verbose_name_plural = 'Telegram Bots'

	def __str__(self):
		return f'ID: {self.id} | Имя бота: {self.name} | Запушен ли бот: {self.online}'

class TelegramBotLogModel(models.Model):
	bot = models.ForeignKey(TelegramBotModel, on_delete=models.CASCADE)
	user_name = models.CharField(max_length=256)
	user_message = models.TextField()

class TelegramBotCommandModel(models.Model):
	bot = models.ForeignKey(TelegramBotModel, on_delete=models.CASCADE)
	command = models.CharField(max_length=256)
	command_answer = models.TextField()