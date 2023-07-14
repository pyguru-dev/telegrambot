from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.conf import settings

from .managers import UserManager

from constructor_telegram_bots.functions import generate_random_string
from constructor_telegram_bots import environment


class User(AbstractBaseUser, PermissionsMixin):
	telegram_id = models.BigIntegerField('Telegram ID', unique=True, null=True)
	username = models.CharField(_('Имя пользователя'), max_length=32, unique=True, null=True)
	password = None
	is_staff = models.BooleanField(_('Сотрудник'), default=False)
	confirm_code = models.CharField(max_length=25, unique=True, null=True)
	date_joined = models.DateTimeField(_('Дата присоединения'), auto_now_add=True)

	USERNAME_FIELD = 'username'

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

		return f'{settings.SITE_DOMAIN}user/login/{self.id}/{self.confirm_code}/'

	@property
	async def alogin_url(self) -> str:
		if not self.confirm_code:
			self.confirm_code = generate_random_string(length=25, chars='abcdefghijklnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890')
			await self.asave()

		return f'{settings.SITE_DOMAIN}user/login/{self.id}/{self.confirm_code}/'

	def get_telegram_bots_as_dict(self) -> list:
		return [telegram_bot.to_dict() for telegram_bot in self.telegram_bots.all()]

	def delete(self) -> None:
		environment.delete_user(self)
		super().delete()

	def __str__(self) -> str:
		return self.username
