from django.contrib.auth.base_user import BaseUserManager
from django.conf import settings

import user.models as UserModels

import scripts.functions as Functions

class UserManager(BaseUserManager):	
	def create_user(self, user_id: int, username: str, **extra_fields):
		user: UserModels.User = self.model(id=user_id, username=username, **extra_fields)
		user.save()

		return user

	def create_superuser(user, id: int, username: str, **extra_fields):
		user: UserModels.User = user.create_user(user_id=id, username=username, **extra_fields)
		user.is_staff = True
		user.is_superuser = True
		user.save()

		return user
	
	def get_auth_url(self, user_id: int) -> str:
		user: UserModels.User = self.get(id=user_id)
		user.confirm_code = Functions.generator_secret_string(length=25, chars='abcdefghijklnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890')
		user.save()

		return f'{settings.SITE_DOMAIN}user/auth/{user_id}/{user.confirm_code}/'