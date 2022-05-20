from django.db import models

# Create your models here.
class TelegramBot(models.Model):
	owner = models.CharField(max_length=256)
	bot_name = models.CharField(max_length=20)
	bot_token = models.TextField()

	def __str__(self):
		return self.bot_name