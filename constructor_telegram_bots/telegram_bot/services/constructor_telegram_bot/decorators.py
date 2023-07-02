from aiogram import types

from django.contrib.auth.models import UserManager

from user.models import User

from asgiref.sync import sync_to_async

from functools import wraps


def check_user(func):
	@wraps(func)
	async def wrapper(*args, **kwargs):
		message: types.Message = args[1]

		user: UserManager = await sync_to_async(User.objects.filter)(id=message.from_user.id)

		if await user.aexists() is False:
			await sync_to_async(User.objects.create_user)(user_id=message.from_user.id)

		return await func(*args, **kwargs)
	return wrapper
