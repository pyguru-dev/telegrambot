from django.contrib.auth.base_user import BaseUserManager

import user.models as UserModels


class UserManager(BaseUserManager):	
	def create_user(self, user_id: int, **extra_fields) -> 'UserModels.User':
		return self.create(id=user_id, **extra_fields)

	def create_superuser(self, **fields) -> None:
		return None
