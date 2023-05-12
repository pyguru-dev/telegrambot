from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.core.handlers.wsgi import WSGIRequest
from django.contrib.auth import login, logout
from django.shortcuts import HttpResponse, render

from user.models import User

import json


def user_login(request: WSGIRequest, user_id: int, confirm_code: str) -> HttpResponse:
	if User.objects.filter(id=user_id).exists():
		user: User = User.objects.get(id=user_id)
		if user.confirm_code == confirm_code:
			user.confirm_code = None
			user.save()

			login(request=request, user=user)

			context = {'heading': 'Успешная авторизация'}
		else:
			context = {'heading': 'Неверный код подтверждения!'}
	else:
		context = {'heading': 'Не удалось найти пользователя!'}

	return render(request=request, template_name='login.html', context=context)

@csrf_exempt
@login_required
def user_logout(request: WSGIRequest) -> HttpResponse:
	logout(request=request)

	return render(request=request, template_name='logout.html')


@csrf_exempt
@login_required
def get_user_telegram_bots(request: WSGIRequest) -> HttpResponse:
	added_telegram_bots = []
	for telegram_bot in request.user.telegram_bots.all():
		added_telegram_bots.append(
			{
				'id': telegram_bot.id,
				'name': telegram_bot.name,
				'api_token': telegram_bot.api_token,
				'commands_count': telegram_bot.commands.count(),
				'users_count': telegram_bot.users.count(),
				'date_added': telegram_bot.date_added.strftime('%d %B %Y г. %H:%M'),

			}
		)

	return HttpResponse(json.dumps(added_telegram_bots))
