from django.views.decorators.csrf import csrf_exempt
from django.core.handlers.wsgi import WSGIRequest
from django.shortcuts import HttpResponse
from django.shortcuts import render
from django.contrib.auth import login

from user.models import User

import scripts.decorators as Decorators

# Create your views here.
@Decorators.get_user_data
def auth(request: WSGIRequest, user_id: int, confirm_code: str, data: dict):
	if User.objects.filter(id=user_id).exists():
		user = User.objects.get(id=user_id)

		if user.confirm_code == confirm_code:
			user.confirm_code = None
			user.save()

			login(request=request, user=user)

			data.update(
				{
					'title': 'Авторизация',
					'meta': {
						'url': '/personal_cabinet/',
					},
					'content': {
						'heading': 'Успешная авторизация.',
						'text': 'Автоматический переход в личный кабинет через 3 секунды.',
					},
				}
			)
		else:
			data.update(
				{
					'title': 'Авторизация',
					'meta': {
						'url': '/',
					},
					'content': {
						'heading': 'Неверный пароль!',
						'text': 'Автоматический переход на главную страницу через 3 секунды.',
					},
				}
			)
	else:
		data.update(
			{
				'title': 'Авторизация',
				'meta': {
					'url': '/',
				},
				'content': {
					'heading': 'Не удалось найти пользователя!',
					'text': 'Автоматический переход на главную страницу через 3 секунды.',
				},
			}
		)

	return render(request, '.html', context=data)

@csrf_exempt
@Decorators.is_auth(render_page=False)
def get_added_telegram_bots(request: WSGIRequest):
	added_telegram_bots = ''
	for telegram_bot in request.user.telegram_bots.all():
		added_telegram_bots += f'''\
			<div class="col py-2">
				<div class="card">
					<div class="card-header h5 bg-danger text-center text-light fw-bold">Бот выключен</div>
					<div class="<div class="card-body">
						<p class="h5 card-title text-center p-2 mb-1">@<a class="link-dark" href="tg://resolve?domain={telegram_bot.name}">{telegram_bot.name}</a></p>
					</div>
					<div class="card-footer">
						<a class="btn btn-outline-dark my-1 w-100" href="/personal_cabinet/{telegram_bot.id}/">Меню Telegram бота</a>
					</div>
				</div>
			</div>
		'''

	return HttpResponse(added_telegram_bots)