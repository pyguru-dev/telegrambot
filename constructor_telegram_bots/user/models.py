from django.db import models
from django.contrib.auth.models import AbstractUser

from telegram_bot.models import TelegramBot

# Create your models here.
class User(AbstractUser):
	telegram_bots = models.ManyToManyField(TelegramBot)