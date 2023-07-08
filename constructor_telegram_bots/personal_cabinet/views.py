from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from django.contrib.auth.decorators import login_required
from telegram_bot.decorators import check_telegram_bot_id

from telegram_bot.models import TelegramBot


@login_required
def personal_cabinet(request: HttpRequest) -> HttpResponse:
	return render(request, 'personal_cabinet/main.html')

@login_required
@check_telegram_bot_id
def telegram_bot_menu(request: HttpRequest, telegram_bot: TelegramBot) -> HttpResponse:
	return render(request, 'telegram_bot_menu/main.html', {'telegram_bot': telegram_bot})
