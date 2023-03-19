from django.views.decorators.csrf import csrf_exempt
from django.core.handlers.wsgi import WSGIRequest
from django.shortcuts import HttpResponse

from telegram_bot.models import TelegramBot, TelegramBotCommand, TelegramBotUser

from scripts.decorators import SiteDecorators

import json

@csrf_exempt
@SiteDecorators.is_auth(render_page=False)
@SiteDecorators.check_request_data_items(needs_items=('token', 'private',))
@SiteDecorators.check_telegram_bot_token
def add_telegram_bot(request: WSGIRequest, token: str, private: bool) -> HttpResponse:
	TelegramBot.objects.add_telegram_bot(request=request, token=token, private=private)

	return HttpResponse('Вы успешно добавили Telegram бота.')

@csrf_exempt
@SiteDecorators.is_auth(render_page=False)
@SiteDecorators.check_telegram_bot_id(render_page=False)
@SiteDecorators.check_request_data_items(needs_items=('token', 'private',))
@SiteDecorators.check_telegram_bot_token
def duplicate_telegram_bot(request: WSGIRequest, telegram_bot: TelegramBot, token: str, private: bool) -> HttpResponse:
	TelegramBot.objects.duplicate_telegram_bot(request=request, telegram_bot=telegram_bot, token=token, private=private)

	return HttpResponse('Вы успешно дублировали Telegram бота.')

@csrf_exempt
@SiteDecorators.is_auth(render_page=False)
@SiteDecorators.check_telegram_bot_id(render_page=False)
def delete_telegram_bot(request: WSGIRequest, telegram_bot: TelegramBot) -> HttpResponse:
	TelegramBot.objects.delete_telegram_bot(telegram_bot=telegram_bot)

	return HttpResponse('Вы успешно удалили Telegram бота.')

@csrf_exempt
@SiteDecorators.is_auth(render_page=False)
@SiteDecorators.check_telegram_bot_id(render_page=False)
def start_telegram_bot(request: WSGIRequest, telegram_bot: TelegramBot) -> HttpResponse:
	telegram_bot.is_running = True
	telegram_bot.save()

	return HttpResponse('Вы успешно включили Telegram бота.')

@csrf_exempt
@SiteDecorators.is_auth(render_page=False)
@SiteDecorators.check_telegram_bot_id(render_page=False)
def stop_telegram_bot(request: WSGIRequest, telegram_bot: TelegramBot) -> HttpResponse:
	telegram_bot.is_running = False
	telegram_bot.save()

	return HttpResponse('Вы успешно выключили Telegram бота.')

@csrf_exempt
@SiteDecorators.is_auth(render_page=False)
@SiteDecorators.check_telegram_bot_id(render_page=False)
@SiteDecorators.check_request_data_items(needs_items=('telegram_bot_private',))
def edit_telegram_bot_private(request: WSGIRequest, telegram_bot: TelegramBot, telegram_bot_private: bool) -> HttpResponse:
	telegram_bot.private = telegram_bot_private
	telegram_bot.save()

	return HttpResponse(f"Вы успешно сделали своего Telegram бота {'не' if telegram_bot_private == False else ''} приватным.")

@csrf_exempt
@SiteDecorators.is_auth(render_page=False)
@SiteDecorators.check_telegram_bot_id(render_page=False)
@SiteDecorators.check_request_data_items(needs_items=('name', 'command', 'callback', 'message_text', 'is_edit_last_message', 'keyboard',))
@SiteDecorators.check_data_for_telegram_bot_command
def add_telegram_bot_command(request: WSGIRequest, telegram_bot: TelegramBot, name: str, command: str, callback: str, message_text: str, is_edit_last_message: bool, keyboard: str) -> HttpResponse:
	TelegramBotCommand.objects.add_telegram_bot_command(telegram_bot=telegram_bot, name=name, command=command, callback=callback, message_text=message_text, is_edit_last_message=is_edit_last_message, keyboard=keyboard)

	return HttpResponse('Вы успешно добавили команду Telegram боту.')

@csrf_exempt
@SiteDecorators.is_auth(render_page=False)
@SiteDecorators.check_telegram_bot_id(render_page=False)
@SiteDecorators.check_telegram_bot_command_id
@SiteDecorators.check_request_data_items(needs_items=('name', 'command', 'callback', 'message_text', 'is_edit_last_message', 'keyboard',))
@SiteDecorators.check_data_for_telegram_bot_command
def edit_telegram_bot_command(request: WSGIRequest, telegram_bot: TelegramBot, telegram_bot_command: TelegramBotCommand, name: str, command: str, callback: str, message_text: str, is_edit_last_message: bool, keyboard: str) -> HttpResponse:
	telegram_bot_command.name = name
	telegram_bot_command.command = command
	telegram_bot_command.callback = callback
	telegram_bot_command.message_text = message_text
	telegram_bot_command.is_edit_last_message = is_edit_last_message
	telegram_bot_command.keyboard = keyboard
	telegram_bot_command.save()

	return HttpResponse('Вы успешно изменили команду Telegram бота.')

@csrf_exempt
@SiteDecorators.is_auth(render_page=False)
@SiteDecorators.check_telegram_bot_id(render_page=False)
@SiteDecorators.check_telegram_bot_command_id
def delete_telegram_bot_command(request: WSGIRequest, telegram_bot: TelegramBot, telegram_bot_command: TelegramBotCommand) -> HttpResponse:
	telegram_bot_command.delete()

	return HttpResponse('Вы успешно удалили команду Telegram бота.')

@csrf_exempt
@SiteDecorators.is_auth(render_page=False)
@SiteDecorators.check_telegram_bot_id(render_page=False)
@SiteDecorators.check_telegram_bot_user_id
def give_telegram_bot_user_access(request: WSGIRequest, telegram_bot: TelegramBot, telegram_bot_user: TelegramBotUser) -> HttpResponse:
	telegram_bot.allowed_users.add(telegram_bot_user)
	telegram_bot.save()

	return HttpResponse('Вы успешно выдали доступ пользователю к Telegram боту.')

@csrf_exempt
@SiteDecorators.is_auth(render_page=False)
@SiteDecorators.check_telegram_bot_id(render_page=False)
@SiteDecorators.check_telegram_bot_user_id
def delete_telegram_bot_user(request: WSGIRequest, telegram_bot: TelegramBot, telegram_bot_user: TelegramBotUser) -> HttpResponse:
	telegram_bot_user.delete()

	return HttpResponse('Вы успешно удалили пользователя Telegram бота.')

@csrf_exempt
@SiteDecorators.is_auth(render_page=False)
@SiteDecorators.check_telegram_bot_id(render_page=False)
def get_telegram_bot_commands(request: WSGIRequest, telegram_bot: TelegramBot) -> HttpResponse:
	telegram_bot_commands = {}
	for telegram_bot_command in telegram_bot.commands.all():
		telegram_bot_commands.update(
			{
				telegram_bot_command.id: telegram_bot_command.name,
			}
		)

	return HttpResponse(
		json.dumps(telegram_bot_commands)
	)

@csrf_exempt
@SiteDecorators.is_auth(render_page=False)
@SiteDecorators.check_telegram_bot_id(render_page=False)
@SiteDecorators.check_telegram_bot_command_id
def get_telegram_bot_command_data(request: WSGIRequest, telegram_bot: TelegramBot, telegram_bot_command: TelegramBotCommand) -> HttpResponse:
	return HttpResponse(
		json.dumps(
			{
				'name': telegram_bot_command.name,
				'command': telegram_bot_command.command,
				'callback': telegram_bot_command.callback,
				'message_text': telegram_bot_command.message_text,
				'is_edit_last_message': telegram_bot_command.is_edit_last_message,
				'keyboard': telegram_bot_command.keyboard,
			}
		)
	)

@csrf_exempt
@SiteDecorators.is_auth(render_page=False)
@SiteDecorators.check_telegram_bot_id(render_page=False)
def get_telegram_bot_users(request: WSGIRequest, telegram_bot: TelegramBot) -> HttpResponse:
	telegram_bot_users = {}
	for telegram_bot_user in telegram_bot.users.all():
		telegram_bot_users.update(
			{
				telegram_bot_user.id: {
					'username': telegram_bot_user.username,
					'date_started': telegram_bot_user.date_started.strftime('%H:%M:%S - %d.%m.%Y'),
				}
			}
		)

	return HttpResponse(
		json.dumps(telegram_bot_users)
	)