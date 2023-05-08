from django.contrib.auth.decorators import login_required
from django.core.handlers.wsgi import WSGIRequest
from django.shortcuts import HttpResponse, render

from telegram_bot.models import TelegramBot

from telegram_bot.decorators import check_telegram_bot_id


@login_required
def personal_cabinet(request: WSGIRequest) -> HttpResponse:
	return render(request=request, template_name='personal_cabinet/main.html')

@login_required
@check_telegram_bot_id
def telegram_bot_menu(request: WSGIRequest, telegram_bot: TelegramBot) -> HttpResponse:
	return render(request=request, template_name='telegram_bot_menu/main.html', context={'telegram_bot': telegram_bot})
