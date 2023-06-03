from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponseBadRequest

from django.core.exceptions import RequestDataTooBig

from django.views.decorators.http import require_POST

from functools import wraps
import json


def check_post_request_data_items(request_need_items: tuple):
	def decorator(func):
		@require_POST
		@wraps(func)
		def wrapper(*args, **kwargs):
			request: WSGIRequest = args[0]

			try:
				request_data: dict = json.loads(request.body)
			except (UnicodeDecodeError, json.decoder.JSONDecodeError):
				request_data: dict = json.loads(request.POST['data'])
			except RequestDataTooBig:
				return HttpResponseBadRequest('Тело запроса не должно весить больше 2.5MB!')

			request_data_items: tuple = tuple([request_data_item for request_data_item in tuple(request_data.keys()) if request_data_item in request_need_items])

			if request_data_items == request_need_items:
				for request_data_item in request_data_items:
					kwargs.update({request_data_item: request_data[request_data_item]})

				return func(*args, **kwargs)
			else:
				return HttpResponseBadRequest('В тело запроса переданы не все нужные данные!')
		return wrapper
	return decorator
