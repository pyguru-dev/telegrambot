from django.utils.datastructures import MultiValueDictKeyError
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
				try:
					request_data: dict = json.loads(request.POST['data'])
				except MultiValueDictKeyError:
					return Response({
						'message': _('В тело запроса переданы не все данные!'),
						'level': 'danger',
					}, status=400)
			except RequestDataTooBig:
				return Response({
					'message': _('Тело запроса не должно весить больше 2.5MB!'),
					'level': 'danger',
				}, status=400)
			except:
				return Response({
					'message': _('На стороне сайта произошла непредвиденная ошибка, попробуйте ещё раз позже!'),
					'level': 'danger',
				}, status=500)

			delete_request_data_items = []

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
					delete_request_data_items.append(key)

			for delete_request_data_item in delete_request_data_items:
				del request_data[delete_request_data_item]

			if needed_request_data.keys() != request_data.keys():
				return Response({
					'message': _('В тело запроса переданы не все данные!'),
					'level': 'danger',
				}, status=400)

			return func(*args, **kwargs, **request_data)
		return wrapper
	return decorator
