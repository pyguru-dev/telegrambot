from django.contrib.auth.base_user import BaseUserManager

import user.models as UserModels


class UserManager(BaseUserManager):	
	def create_user(self, user_id: int, **extra_fields) -> 'UserModels.User':
		user: UserModels.User = self.model(id=user_id, **extra_fields)
		user.save()

		return user

	def create_superuser(self, username: int, password: str, **extra_fields) -> 'UserModels.User':
		user: UserModels.User = self.model(
			username=username,
			password=password,
			is_superuser=True,
			is_staff=True,
			**extra_fields
		)
		user.save()

		return user
