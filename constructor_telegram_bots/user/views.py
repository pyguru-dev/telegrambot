from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.core.handlers.wsgi import WSGIRequest
from django.shortcuts import HttpResponse, render
from django.contrib.auth import login

from user.models import User

import json


def user_auth(request: WSGIRequest, user_id: int, confirm_code: str) -> HttpResponse:
	context = {
		'title': 'Авторизация',
		'meta': {
			'url': '/',
		},
		'content': {
			'text': 'Автоматический переход на главную страницу через 3 секунды.',
		},
	}
	
	if User.objects.filter(id=user_id).exists():
		user: User = User.objects.get(id=user_id)
		if user.confirm_code == confirm_code:
			user.confirm_code = None
			user.save()

			login(request=request, user=user)

			context.update(
				{
					'meta': {
						'url': '/personal-cabinet/',
					},
					'content': {
						'heading': 'Успешная авторизация.',
						'text': 'Автоматический переход в личный кабинет через 3 секунды.',
					},
				}
			)
		else:
			context.update(
				{
					'content': {
						'text': 'Автоматический переход на главную страницу через 3 секунды.',
					},
				}
			)
	else:
		context.update(
			{
				'content': {
					'text': 'Автоматический переход на главную страницу через 3 секунды.',
				},
			}
		)

	return render(request=request, template_name='auth.html', context=context)

@csrf_exempt
@login_required
def get_user_added_telegram_bots(request: WSGIRequest) -> HttpResponse:
	added_telegram_bots = {}
	for telegram_bot in request.user.telegram_bots.all():
		added_telegram_bots.update(
			{
				telegram_bot.id: {
					'name': telegram_bot.name,
					'is_running': telegram_bot.is_running,
				},
			}
		)

	return HttpResponse(json.dumps(added_telegram_bots))
