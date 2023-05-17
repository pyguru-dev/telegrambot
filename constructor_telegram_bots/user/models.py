from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db.models import CharField, BooleanField, ManyToManyField, DateTimeField

from telegram_bot.models import TelegramBot
from user.managers import UserManager

from constructor_telegram_bots.functions import generate_random_string

from django.conf import settings


class User(AbstractBaseUser, PermissionsMixin):
	password = None
	confirm_code = CharField(max_length=25, null=True)
	is_staff = BooleanField(default=False)
	telegram_bots = ManyToManyField(TelegramBot, related_name='telegram_bots')
	date_joined = DateTimeField(auto_now_add=True)

	USERNAME_FIELD = 'id'

	objects = UserManager()

	class Meta:
		db_table = 'user'

	def get_login_url(self) -> str:
		self.confirm_code = generate_random_string(length=25, chars='abcdefghijklnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890')
		self.save()

		return f'{settings.SITE_DOMAIN}user/login/{self.id}/{self.confirm_code}/'
	
	def delete(self) -> None:
		for telegram_bot in self.telegram_bots.all():
			telegram_bot.delete()

		super().delete()
