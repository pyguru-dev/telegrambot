from django.core.handlers.wsgi import WSGIRequest
from django.contrib.auth import login
from django.shortcuts import render

from user.models import User

import scripts.decorators as Decorators

# Create your views here.
@Decorators.get_user_data
def auth(request: WSGIRequest, user_id: int, password: str, data: dict):
	if User.objects.filter(id=user_id).exists():
		user = User.objects.get(id=user_id)

		if user.password == password:
			login(request=request, user=user)

			data.update(
				{
					'meta': {
						'url': '/personal_cabinet/',
					},
					'content': {
						'heading': 'Успешная авторизация.',
						'text': 'Автоматически переход в личный кабинет через 3 секунд.',
					},
				}
			)
		else:
			data.update(
				{
					'meta': {
						'url': '/',
					},
					'content': {
						'heading': 'Неверный пароль!',
						'text': 'Автоматически переход на главную страницу через 3 секунд.',
					},
				}
			)
	else:
		data.update(
				{
					'meta': {
						'url': '/',
					},
					'content': {
						'heading': 'Не удалось найти пользователя!',
						'text': 'Автоматически переход на главную страницу через 3 секунд.',
					},
				}
			)

	return render(request, 'auth.html', context=data)