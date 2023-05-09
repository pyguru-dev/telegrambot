from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.conf import settings
from django.db import models

from telegram_bot.models import TelegramBot
from user.managers import UserManager

from constructor_telegram_bots.functions import generate_random_string


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

	def get_login_url(self) -> str:
		self.confirm_code = generate_random_string(length=25, chars='abcdefghijklnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890')
		self.save()

		return f'{settings.SITE_DOMAIN}user/login/{self.id}/{self.confirm_code}/'
