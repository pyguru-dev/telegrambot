from django.core.handlers.wsgi import WSGIRequest
from django.http import JsonResponse

from django.utils.translation import gettext

from django.core.exceptions import RequestDataTooBig

from functools import wraps
import json


def check_post_request_data_items(request_need_items: tuple):
	def decorator(func):
		@wraps(func)
		def wrapper(*args, **kwargs):
			request: WSGIRequest = args[0]

			try:
				request_data: dict = json.loads(request.body)
			except (UnicodeDecodeError, json.decoder.JSONDecodeError):
				request_data: dict = json.loads(request.POST['data'])
			except RequestDataTooBig:
				return JsonResponse(
					{
						'message': gettext('Тело запроса не должно весить больше 2.5MB!'),
						'level': 'danger',
					},
					status_code=400
				)

			request_data_items: tuple = tuple([request_data_item for request_data_item in tuple(request_data.keys()) if request_data_item in request_need_items])

			if request_data_items == request_need_items:
				for request_data_item in request_data_items:
					kwargs.update({request_data_item: request_data[request_data_item]})

				return func(*args, **kwargs)
			else:
				return JsonResponse(
					{
						'message': gettext('В тело запроса переданы не все нужные данные!'),
						'level': 'danger',
					},
					status_code=400
				)
		return wrapper
	return decorator
