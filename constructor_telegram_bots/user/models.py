from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models

from user.managers import UserManager

from constructor_telegram_bots.functions import generate_random_string

from django.conf import settings


class User(AbstractBaseUser, PermissionsMixin):
	username = models.CharField(max_length=32, unique=True, null=True)
	password = models.CharField(max_length=25, null=True)
	confirm_code = models.CharField(max_length=25, unique=True, null=True)
	date_joined = models.DateTimeField(auto_now_add=True)

	USERNAME_FIELD = 'username'
	REQUIRED_FIELDS = ['password']

	objects = UserManager()

	class Meta:
		db_table = 'user'

	@property
	def login_url(self) -> str:
		if not self.confirm_code:
			self.confirm_code = generate_random_string(length=25, chars='abcdefghijklnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890')
			self.save()

		return f'{settings.SITE_DOMAIN}user/login/{self.id}/{self.confirm_code}/'
	
	@property
	async def alogin_url(self) -> str:
		if not self.confirm_code:
			self.confirm_code = generate_random_string(length=25, chars='abcdefghijklnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890')
			await self.asave()

		return f'{settings.SITE_DOMAIN}user/login/{self.id}/{self.confirm_code}/'

	def get_telegram_bots_as_dict(self) -> list:
		return [telegram_bot.to_dict() for telegram_bot in self.telegram_bots.all()]
