from django.utils.translation import gettext as _

from rest_framework.response import Response

from telegram_bot.models import TelegramBot

from .models import Plugin

from typing import Optional
from functools import wraps
import re


def check_plugin_id(func):
	@wraps(func)
	def wrapper(*args, **kwargs):
		plugin_id: int = kwargs.pop('plugin_id')

		if not Plugin.objects.filter(id=plugin_id).exists():
			return Response({
				'message': _('Плагин не найден!'),
				'level': 'danger',
			}, status=404)

		return func(plugin=Plugin.objects.get(id=plugin_id), *args, **kwargs)
	return wrapper

def check_plugin_data(func):
	@wraps(func)
	def wrapper(*args, **kwargs):
		telegram_bot: TelegramBot = kwargs['telegram_bot'] if 'telegram_bot' in kwargs else kwargs['plugin'].telegram_bot
		name: Optional[str] = kwargs['name'] if 'name' in kwargs else None
		code: str = kwargs['code']

		if name is not None:
			if name:
				return Response({
					'message': _('Введите название плагина!'),
					'level': 'danger',
				}, status=400)

			if len(name) > 255:
				return Response({
					'message': _('Название плагина должно содержать не более 255 символов!'),
					'level': 'danger',
				}, status=400)

			if re.match(r'^[a-zA-Z_][a-zA-Z0-9_]*$', name) is None:
				return Response({
					'message': _('Название плагина содержит запрещенные символы!'),
					'level': 'danger',
				}, status=400)

		if Plugin.objects.filter(telegram_bot=telegram_bot, name=name).exists():
			return Response({
				'message': _('У вас уже добавлен плагин с таким названием!'),
				'level': 'danger',
			}, status=400)

		if not code:
			return Response({
				'message': _('Введите код плагина!'),
				'level': 'danger',
			}, status=400)

		return func(*args, **kwargs)
	return wrapper
