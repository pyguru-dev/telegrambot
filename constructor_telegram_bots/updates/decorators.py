from django.http import JsonResponse
from django.utils.translation import gettext as _

from rest_framework.status import *

from .models import Update

from functools import wraps


def check_update_id(func):
	@wraps(func)
	def wrapper(*args, **kwargs):
		update_id: int = kwargs.pop('update_id')

		if not Update.objects.filter(id=update_id).exists():
			return JsonResponse({
				'message': _('Обновление не найдено!'),
				'level': 'danger',
			}, status=HTTP_404_NOT_FOUND)

		return func(update=Update.objects.get(id=update_id), *args, **kwargs)
	return wrapper
