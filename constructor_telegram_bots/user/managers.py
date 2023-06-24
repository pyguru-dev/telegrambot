from django.contrib.auth.base_user import BaseUserManager

import user.models as UserModels


class UserManager(BaseUserManager):	
	def create_user(self, user_id: int, **extra_fields) -> 'UserModels.User':
		return self.create(id=user_id, **extra_fields)

	def create_superuser(self, username: int, password: str, **extra_fields) -> 'UserModels.User':
		return self.create(
			username=username,
			password=password,
			is_staff=True,
			is_superuser=True,
			**extra_fields
		)
