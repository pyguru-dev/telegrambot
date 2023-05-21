from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponseBadRequest

import json


def check_post_request_data_items(request_need_items: tuple):
	def decorator(func):
		def wrapper(*args, **kwargs):
			request: WSGIRequest = args[0]

			if request.method == 'POST':
				request_data: dict = json.loads(request.body)
				request_data_items: tuple = tuple([request_data_item for request_data_item in tuple(request_data.keys()) if request_data_item in request_need_items])

				if request_data_items == request_need_items:
					for request_data_item in request_data_items:
						kwargs.update({request_data_item: request_data[request_data_item]})

					return func(*args, **kwargs)
				else:
					return HttpResponseBadRequest('В тело запроса переданы не все данные!')
			else:
				return HttpResponseBadRequest('Неправильный метод запроса!')
		return wrapper
	return decorator
