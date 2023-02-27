from django.contrib.auth.base_user import BaseUserManager

import scripts.functions as Functions

class UserManager(BaseUserManager):	
	def create_user(self, user_id: int, username: str, **extra_fields):
		user = self.model(id=user_id, username=username, **extra_fields)
		user.save()

		return user

	def create_superuser(user, id: int, username: str, **extra_fields):
		user = user.create_user(user_id=id, username=username)
		user.is_staff = True
		user.is_superuser = True
		user.save()

		return user
	
	def get_auth_url(self, user_id: int):
		user = self.get(id=user_id)
		user.confirm_code = Functions.generator_secret_string(length=25, chars='abcdefghijklnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890')
		user.save()

		return f'http://127.0.0.1:8000/user/auth/{user_id}/{user.confirm_code}/'