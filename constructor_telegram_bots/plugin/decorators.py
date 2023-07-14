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