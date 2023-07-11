from aiogram import types

from user.models import User, UserManager

from asgiref.sync import sync_to_async
from functools import wraps


def check_user(func):
	@wraps(func)
	async def wrapper(*args, **kwargs):
		message: types.Message = args[1]

		user: UserManager = await sync_to_async(User.objects.filter)(telegram_id=message.from_user.id)

		if await user.aexists() is False:
			await sync_to_async(User.objects.create_user)(telegram_id=message.from_user.id, username=message.from_user.username)

		return await func(*args, **kwargs)
	return wrapper
