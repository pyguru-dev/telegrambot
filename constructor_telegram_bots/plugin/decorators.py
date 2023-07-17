from django.utils.translation import gettext as _

from rest_framework.response import Response

from .models import Plugin

from functools import wraps


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
		code: str = kwargs['code']

		if 'name' in kwargs:
			name: str = kwargs['name']

			if not name:
				if len(name) > 255:
					return Response({
						'message': _('Название плагина должно содержать не более 255 символов!'),
						'level': 'danger',
					}, status=400)
				else:
					return Response({
						'message': _('Введите название плагина!'),
						'level': 'danger',
					}, status=400)

		if not code:
			return Response({
				'message': _('Введите код плагина!'),
				'level': 'danger',
			}, status=400)

		return func(*args, **kwargs)
	return wrapper
