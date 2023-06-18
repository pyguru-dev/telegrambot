from django.core.handlers.wsgi import WSGIRequest
from django.shortcuts import HttpResponse, render
from django.http import JsonResponse

from django.utils.translation import gettext

from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required

from django.contrib.auth import login, logout

from user.models import User


def user_login(request: WSGIRequest, id: int, confirm_code: str) -> HttpResponse:
	if User.objects.filter(id=id).exists():
		user: User = User.objects.get(id=id)
		if user.confirm_code == confirm_code:
			user.confirm_code = None
			user.save()

			login(request, user)

			context = {'heading': gettext('Успешная авторизация')}
		else:
			context = {'heading': gettext('Неверный код подтверждения!')}
	else:
		context = {'heading': gettext('Не удалось найти пользователя!')}

	return render(request, 'login.html', context)

@csrf_exempt
@login_required
def user_logout(request: WSGIRequest) -> HttpResponse:
	logout(request)

	return render(request, 'logout.html')


@csrf_exempt
@require_POST
@login_required
def get_user_telegram_bots(request: WSGIRequest) -> HttpResponse:
	return JsonResponse(
		request.user.get_telegram_bots_as_dict(),
		safe=False
	)