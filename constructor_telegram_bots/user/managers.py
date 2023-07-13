from django.contrib.auth.base_user import BaseUserManager

from rest_framework.authtoken.models import Token

import user.models as UserModels

from constructor_telegram_bots import environment


class UserManager(BaseUserManager):
	def create(self, telegram_id: int, username: str, **extra_fields) -> 'UserModels.User':
		user: UserModels.User = super().create(
			telegram_id=telegram_id,
			username=username,
			**extra_fields
		)
		Token.objects.create(user=user)
		environment.create_user(user)
		return user

	def create_superuser(self, **fields) -> None:
		raise SyntaxError('Not support to create superuser!')
