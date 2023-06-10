from django.core.handlers.wsgi import WSGIRequest
from django.shortcuts import HttpResponse, render

from user.models import User
from telegram_bot.models import TelegramBot


def home(request: WSGIRequest) -> HttpResponse:
	return render(
		request,
		'home.html',
		{
			'users_count': User.objects.count(),
			'telegram_bots_count': TelegramBot.objects.count(),
		}
	)
