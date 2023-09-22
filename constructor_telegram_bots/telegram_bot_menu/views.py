from django.http import HttpRequest, HttpResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from telegram_bot.decorators import check_telegram_bot_id


@login_required
@check_telegram_bot_id
def telegram_bot_view(request: HttpRequest, **context) -> HttpResponse:
	return render(request, 'telegram_bot.html', context)

@login_required
@check_telegram_bot_id
def telegram_bot_users_view(request: HttpRequest, **context) -> HttpResponse:
	return render(request, 'telegram_bot_users.html', context)

@login_required
@check_telegram_bot_id
def telegram_bot_database_view(request: HttpRequest, **context) -> HttpResponse:
	return render(request, 'telegram_bot_database.html', context)

@login_required
@check_telegram_bot_id
def telegram_bot_plugins_view(request: HttpRequest, **context) -> HttpResponse:
	return render(request, 'telegram_bot_plugins.html', context)

@login_required
@check_telegram_bot_id
def telegram_bot_constructor_view(request: HttpRequest, **context) -> HttpResponse:
	return render(request, 'telegram_bot_constructor/main.html', context)
