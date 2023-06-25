from django.core.handlers.wsgi import WSGIRequest
from django.shortcuts import HttpResponse, render
from django.http import JsonResponse

from django.utils.translation import gettext as _

from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from constructor_telegram_bots.decorators import check_post_request_data_items

from django.contrib.auth import login, logout

from user.models import User, UserManager


@csrf_exempt
@require_POST
@check_post_request_data_items(
	{
		'username': str,
		'password': str,
	}
)
def admin_login(
	request: WSGIRequest,
	username: str,
	password: str
):
	if username == '':
		return JsonResponse(
			{
				'message': 'Введите имя пользователя!',
				'level': 'danger',
			},
			status=400
		)
	elif password == '':
		return JsonResponse(
			{
				'message': 'Введите пароль!',
				'level': 'danger',
			},
			status=400
		)
	
	user: UserManager = User.objects.filter(
		username=username,
		password=password
	)

	if user.exists():
		user: User = user.first()

		if user.is_staff:			
			login(request, user)

			return JsonResponse(
				{
					'message': 'Вы успешно авторизовались.',
					'level': 'success',
				}
			)
		else:
			return JsonResponse(
				{
					'message': 'Вы не имеете доступ к администрированию сайта!',
					'level': 'danger',
				},
				status=400
			)
	else:
		return JsonResponse(
			{
				'message': 'Пользователь не найден!',
				'level': 'danger',
			},
			status=400
		)


def user_login(request: WSGIRequest, id: int, confirm_code: str) -> HttpResponse:
	if User.objects.filter(id=id).exists():
		user: User = User.objects.get(id=id)
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