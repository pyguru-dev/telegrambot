from django.contrib.auth.base_user import BaseUserManager

import user.models as UserModels


class UserManager(BaseUserManager):	
	def create_user(self, user_id: int, **extra_fields):
		user: UserModels.User = self.model(id=user_id, **extra_fields)
		user.save()

		return user

	def create_superuser(user, user_id: int, **extra_fields):
		user: UserModels.User = user.create_user(user_id=user_id, **extra_fields)
		user.is_staff = True
		user.is_superuser = True
		user.save()

		return user
