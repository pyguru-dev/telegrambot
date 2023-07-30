from django.core.exceptions import RequestDataTooBig
from django.utils.translation import gettext as _

from rest_framework.request import Request
from rest_framework.response import Response

from functools import wraps
import json


def check_post_request_data_items(needed_request_data: dict):
	def decorator(func):
		@wraps(func)
		def wrapper(*args, **kwargs):
			request: Request = args[-1]

			try:
				request_data: dict = json.loads(request.body)
			except (UnicodeDecodeError, json.decoder.JSONDecodeError):
				request_data: dict = json.loads(request.POST['data'])
			except RequestDataTooBig:
				return Response({
					'message': _('Тело запроса не должно весить больше 2.5MB!'),
					'level': 'danger',
				}, status=400)

			request_data_delete_items = []

			for key, value in request_data.items():
				if key == 'image':
					continue

				if key in needed_request_data:
					if not isinstance(value, needed_request_data[key]):
						return Response({
							'message': _('В тело запроса передан неверный тип данных!'),
							'level': 'danger',
						}, status=400)
				else:
					request_data_delete_items.append(key)

			for request_data_delete_item in request_data_delete_items:
				del request_data[request_data_delete_item]

			return func(*args, **kwargs, **request_data)
		return wrapper
	return decorator
