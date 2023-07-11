from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from django.utils.translation import gettext as _

from django.contrib.auth.decorators import login_required

from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response

from user.models import User

from django.contrib.auth import login, logout


def user_login(request: HttpRequest, telegram_id: int, confirm_code: str) -> HttpResponse:
	if User.objects.filter(telegram_id=telegram_id).exists():
		user: User = User.objects.get(telegram_id=telegram_id)

		if user.confirm_code == confirm_code:
			user.confirm_code = None
			user.save()

			login(request, user)

			context = {'heading': _('Успешная авторизация')}
		else:
			context = {'heading': _('Неверный код подтверждения!')}
	else:
		context = {'heading': _('Не удалось найти пользователя!')}

	return render(request, 'login.html', context)

@login_required
def user_logout(request: HttpRequest) -> HttpResponse:
	logout(request)

	return render(request, 'logout.html')


@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_user_telegram_bots(request: Request) -> Response:
	return Response(request.user.get_telegram_bots_as_dict())
