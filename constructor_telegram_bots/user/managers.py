from django.contrib.auth.base_user import BaseUserManager

from rest_framework.authtoken.models import Token

import user.models as UserModels


class UserManager(BaseUserManager):
	def create(self, **fields) -> 'UserModels.User':
		user: UserModels.User = super().create(**fields)
		Token.objects.create(user=user)
		return user

	def create_user(self, user_id: int, **extra_fields) -> 'UserModels.User':
		return self.create(id=user_id, **extra_fields)

	def create_superuser(self, **fields) -> None:
		raise SyntaxError('Not support to create superuser!')
