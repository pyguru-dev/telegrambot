from django.http import HttpRequest, HttpResponse
from django.utils.translation import gettext as _
from django import urls
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required

from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response

from .models import User


def user_login(request: HttpRequest, user_id: int, confirm_code: str) -> HttpResponse:
	context = {
		'title': _('Ошибка авторизации'),
		'meta': {'refresh': {'url': urls.reverse('home')}},
		'content': {'text': _('Автоматический переход на главную страницу через 3 секунды.')},
	}

	if not User.objects.filter(id=user_id).exists():
		context['content']['heading'] = _('Не удалось найти пользователя!')
		return render(request, 'base_success_or_error.html', context)

	user: User = User.objects.get(id=user_id)

	if user.confirm_code != confirm_code:
		context['content']['heading'] = _('Неверный код подтверждения!')
		return render(request, 'base_success_or_error.html', context)

	user.confirm_code = None
	user.save()

	login(request, user)

	return redirect(urls.reverse('personal_cabinet'))

@login_required
def user_logout(request: HttpRequest) -> HttpResponse:
	logout(request)

	return render(request, 'base_success_or_error.html', {
		'title': _('Выход из аккаунта'),
		'meta': {'refresh': {'url': urls.reverse('home')}},
		'content': {
			'heading': _('Успешный выход из аккаунта.'),
			'text': _('Автоматический переход на главную страницу через 3 секунды.'),
		},
	})


@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_user_telegram_bots(request: Request) -> Response:
	return Response(request.user.get_telegram_bots_as_dict())
