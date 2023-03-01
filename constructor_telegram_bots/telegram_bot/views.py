from django.views.decorators.csrf import csrf_exempt
from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponseBadRequest
from django.shortcuts import HttpResponse

from telegram_bot.models import TelegramBot

import scripts.decorators as Decorators

# Create your views here.
@csrf_exempt
@Decorators.is_auth(render_page=False)
@Decorators.check_request_data_items(needs_items=('telegram_bot_token', 'telegram_bot_private',))
def add(request: WSGIRequest, telegram_bot_token: str, telegram_bot_private: bool):
	if TelegramBot.objects.filter(token=telegram_bot_token).exists() == False:
		if TelegramBot.objects.test_telegram_bot_token(token=telegram_bot_token) is not None:
			TelegramBot.objects.add_telegram_bot(request=request, token=telegram_bot_token, private=telegram_bot_private)

			return HttpResponse(f'Вы успешно добавили Telegram бота.')
		else:
			return HttpResponseBadRequest('Ваш токен Telegram бота является недействительным!')
	else:
		return HttpResponseBadRequest('Ваш токен Telegram бота уже использует другой пользователь сайта!')

@csrf_exempt
@Decorators.is_auth(render_page=False)
@Decorators.check_telegram_bot_id(render_page=False)
def delete(request: WSGIRequest, telegram_bot: TelegramBot):
	telegram_bot.delete()

	return HttpResponse(f'Вы успешно удалили @{telegram_bot.name} Telegram бота.')



@csrf_exempt
@Decorators.is_auth(render_page=False)
@Decorators.check_telegram_bot_id(render_page=False)
def start(request: WSGIRequest, telegram_bot: TelegramBot):
	telegram_bot.is_running = True
	telegram_bot.save()

	return HttpResponse(f'Вы успешно включили @{telegram_bot.name} Telegram бота.')

@csrf_exempt
@Decorators.is_auth(render_page=False)
@Decorators.check_telegram_bot_id(render_page=False)
def stop(request: WSGIRequest, telegram_bot: TelegramBot):
	telegram_bot.is_running = False
	telegram_bot.save()

	return HttpResponse(f'Вы успешно выключили @{telegram_bot.name} Telegram бота.')



@csrf_exempt
@Decorators.is_auth(render_page=False)
@Decorators.check_telegram_bot_id(render_page=False)
@Decorators.check_request_data_items(needs_items=('telegram_bot_private',))
def edit_private(request: WSGIRequest, telegram_bot: TelegramBot, telegram_bot_private: bool):
	telegram_bot.private = telegram_bot_private
	telegram_bot.save()

	return HttpResponse(f"Вы успешно сделали вашего @{telegram_bot.name} Telegram бота {'не' if telegram_bot_private == False else ''} приватным.")