from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from django import urls

from rest_framework.authtoken.models import Token

from constructor_telegram_bots.functions import generate_random_string
from constructor_telegram_bots import environment

import requests


class UserManager(BaseUserManager):
	def create(self, telegram_id: int, first_name: str, **extra_fields) -> 'User':
		user: 'User' = super().create(telegram_id=telegram_id, first_name=first_name, **extra_fields)
		Token.objects.create(user=user)
		environment.create_user(user=user)
		return user

	def create_superuser(self, **fields) -> None:
		raise SyntaxError('Not support to create superuser!')

class User(AbstractBaseUser, PermissionsMixin):
	telegram_id = models.BigIntegerField('Telegram ID', unique=True, null=True)
	first_name = models.CharField(_('Имя пользователя'), max_length=64, null=True)
	password = None
	is_staff = models.BooleanField(_('Сотрудник'), default=False)
	confirm_code = models.CharField(max_length=25, unique=True, null=True)
	date_joined = models.DateTimeField(_('Дата присоединения'), auto_now_add=True)

	USERNAME_FIELD = 'telegram_id'

	objects = UserManager()

	class Meta:
		db_table = 'user'

		verbose_name = _('Пользователя')
		verbose_name_plural = _('Пользователи')

	@property
	def login_url(self) -> str:
		if not self.confirm_code:
			self.confirm_code = generate_random_string(length=25, chars='abcdefghijklnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890')
			self.save()
		return f"{settings.SITE_DOMAIN}{urls.reverse('user:login', kwargs={'user_id': self.id, 'confirm_code': self.confirm_code})}"

	@property
	async def alogin_url(self) -> str:
		if not self.confirm_code:
			self.confirm_code = generate_random_string(length=25, chars='abcdefghijklnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890')
			await self.asave()
		return f"{settings.SITE_DOMAIN}{urls.reverse('user:login', kwargs={'user_id': self.id, 'confirm_code': self.confirm_code})}"

	def update_first_name(self) -> None:
		response: requests.Response = requests.get(f'https://api.telegram.org/bot{settings.CONSTRUCTOR_TELEGRAM_BOT_API_TOKEN}/getChat?chat_id={self.telegram_id}')

		if response.status_code == 200:
			first_name: str = response.json()['result']['first_name']

			if self.first_name != first_name:
				self.first_name = first_name
				self.save()

	def get_telegram_bots_as_dict(self) -> list:
		return [telegram_bot.to_dict() for telegram_bot in self.telegram_bots.all()]

	def delete(self) -> None:
		environment.delete_user(self)
		super().delete()

	def __str__(self) -> str:
		return self.first_name
