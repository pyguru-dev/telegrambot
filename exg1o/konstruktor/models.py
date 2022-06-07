from django.db import models
from django.db.models import Max, F

# Create your models here.
class TelegramBot(models.Model):
	id = models.AutoField(primary_key=True)
	owner = models.CharField(max_length=256)
	name = models.CharField(max_length=256)
	token = models.CharField(max_length=256)

	def save(self, *args, **kwargs):
		max = TelegramBot.objects.aggregate(max=Max(F('id')))['max']
		self.id = max + 1 if max else 1
		super().save(*args, **kwargs)

	def __str__(self):
		return f'Владелец: {self.owner} | Бот: {self.name}'

class TelegramBotCommand(models.Model):
	id = models.AutoField(primary_key=True)
	owner = models.CharField(max_length=256)
	bot_name = models.CharField(max_length=256)
	command_name = models.CharField(max_length=29)

	def save(self, *args, **kwargs):
		max = TelegramBotCommand.objects.aggregate(max=Max(F('id')))['max']
		self.id = max + 1 if max else 1
		super().save(*args, **kwargs)

	def __str__(self):
		return f'Владелец: {self.owner} | Бот: {self.bot_name} | Команда: {self.command_name}'