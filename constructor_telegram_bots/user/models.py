from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.conf import settings
from django.db import models

from telegram_bot.models import TelegramBot
from user.managers import UserManager

import scripts.functions as Functions

class User(AbstractBaseUser, PermissionsMixin):
	password = None
	confirm_code = models.CharField(max_length=25, null=True)
	telegram_bots = models.ManyToManyField(TelegramBot, related_name='telegram_bots')
	is_staff = models.BooleanField(default=False)
	date_joined = models.DateTimeField(auto_now_add=True)

	USERNAME_FIELD = 'id'

	objects = UserManager()

	class Meta:
		db_table = 'user'

	def get_auth_url(self) -> str:
		self.confirm_code = Functions.generator_secret_string(length=25, chars='abcdefghijklnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890')
		self.save()

		return f'{settings.SITE_DOMAIN}user/auth/{self.id}/{self.confirm_code}/'
	
	def __str__(self) -> str:
		return str(self.id)