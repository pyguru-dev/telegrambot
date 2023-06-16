from django.core.handlers.wsgi import WSGIRequest
from django.shortcuts import HttpResponse, render
from django.contrib import messages

from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required

from django.contrib.auth import login, logout

from user.models import User

import json


def user_login(request: WSGIRequest, id: int, confirm_code: str) -> HttpResponse:
	if User.objects.filter(id=id).exists():
		user: User = User.objects.get(id=id)
		if user.confirm_code == confirm_code:
			user.confirm_code = None
			user.save()

			login(request, user)

			context = {'heading': 'Успешная авторизация'}
		else:
			context = {'heading': 'Неверный код подтверждения!'}
	else:
		context = {'heading': 'Не удалось найти пользователя!'}

	return render(request, 'login.html', context)

@csrf_exempt
@login_required
def user_logout(request: WSGIRequest) -> HttpResponse:
	logout(request)

	return render(request, 'logout.html')


@csrf_exempt
@login_required
def get_user_messages(request: WSGIRequest) -> HttpResponse:
	messages.info(request=request, message='Тестовая херня)')

	return HttpResponse(
		json.dumps(
			[
				{
				'text': str(message),
				'type': message.tags,
				} for message in messages.get_messages(request=request)
			]
		)
	)

@csrf_exempt
@login_required
def get_user_telegram_bots(request: WSGIRequest) -> HttpResponse:
	return HttpResponse(
		json.dumps(
			request.user.get_telegram_bots_as_dict()
		)
	)