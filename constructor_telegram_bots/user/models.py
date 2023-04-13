from django.contrib.auth.models import AbstractBaseUser
from django.db import models

from telegram_bot.models import TelegramBot
from user.managers import UserManager

class User(AbstractBaseUser):
	password = None
	confirm_code = models.CharField(max_length=25, null=True)
	telegram_bots = models.ManyToManyField(TelegramBot, related_name='telegram_bots')
	is_staff = models.BooleanField(default=False)
	date_joined = models.DateTimeField(auto_now_add=True)

	USERNAME_FIELD = 'id'

	objects = UserManager()