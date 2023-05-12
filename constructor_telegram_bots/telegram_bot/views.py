from django.core.handlers.wsgi import WSGIRequest
from django.shortcuts import HttpResponse
import django.contrib.auth.decorators
import django.views.decorators.csrf

from telegram_bot.models import TelegramBot, TelegramBotCommand, TelegramBotUser

from telegram_bot.telegram_bots.functions import start_telegram_bot as _start_telegram_bot
from telegram_bot.telegram_bots.user_telegram_bot import UserTelegramBot
import constructor_telegram_bots.decorators
import telegram_bot.decorators

import json
import time


@django.views.decorators.csrf.csrf_exempt
@django.contrib.auth.decorators.login_required
@constructor_telegram_bots.decorators.check_post_request_data_items(request_need_items=('api_token', 'is_private',))
@telegram_bot.decorators.check_telegram_bot_api_token
def add_telegram_bot(request: WSGIRequest, api_token: str, is_private: bool) -> HttpResponse:
	TelegramBot.objects.add_telegram_bot(user=request.user, api_token=api_token, is_private=is_private)

	return HttpResponse('Вы успешно добавили Telegram бота.')

@django.views.decorators.csrf.csrf_exempt
@django.contrib.auth.decorators.login_required
@telegram_bot.decorators.check_telegram_bot_id
@constructor_telegram_bots.decorators.check_post_request_data_items(request_need_items=('is_private',))
def edit_telegram_bot(request: WSGIRequest, telegram_bot: TelegramBot, is_private: bool) -> HttpResponse:
	telegram_bot.is_private = is_private
	telegram_bot.save()

	return HttpResponse('Вы успешно изменили Telegram бота.')

@django.views.decorators.csrf.csrf_exempt
@django.contrib.auth.decorators.login_required
@telegram_bot.decorators.check_telegram_bot_id
@constructor_telegram_bots.decorators.check_post_request_data_items(request_need_items=('api_token', 'is_private',))
@telegram_bot.decorators.check_telegram_bot_api_token
def duplicate_telegram_bot(request: WSGIRequest, telegram_bot: TelegramBot, api_token: str, is_private: bool) -> HttpResponse:
	telegram_bot.duplicate(user=request.user, api_token=api_token, is_private=is_private)

	return HttpResponse('Вы успешно дублировали Telegram бота.')

@django.views.decorators.csrf.csrf_exempt
@django.contrib.auth.decorators.login_required
@telegram_bot.decorators.check_telegram_bot_id
def delete_telegram_bot(request: WSGIRequest, telegram_bot: TelegramBot) -> HttpResponse:
	telegram_bot.delete()

	return HttpResponse('Вы успешно удалили Telegram бота.')


@django.views.decorators.csrf.csrf_exempt
@django.contrib.auth.decorators.login_required
@telegram_bot.decorators.check_telegram_bot_id
def start_telegram_bot(request: WSGIRequest, telegram_bot: TelegramBot) -> HttpResponse:
	telegram_bot.is_running = True
	telegram_bot.is_stopped = False
	telegram_bot.save()

	user_telegram_bot = UserTelegramBot(telegram_bot=telegram_bot)
	_start_telegram_bot(telegram_bot=user_telegram_bot)

	return HttpResponse('Вы успешно включили Telegram бота.')

@django.views.decorators.csrf.csrf_exempt
@django.contrib.auth.decorators.login_required
@telegram_bot.decorators.check_telegram_bot_id
def stop_telegram_bot(request: WSGIRequest, telegram_bot: TelegramBot) -> HttpResponse:
	telegram_bot.is_running = False
	telegram_bot.save()

	while True:
		if TelegramBot.objects.get(id=telegram_bot.id).is_stopped:
			break
		else:
			time.sleep(1)

	return HttpResponse('Вы успешно выключили Telegram бота.')


@django.views.decorators.csrf.csrf_exempt
@django.contrib.auth.decorators.login_required
@telegram_bot.decorators.check_telegram_bot_id
@constructor_telegram_bots.decorators.check_post_request_data_items(request_need_items=('name', 'command', 'callback', 'message_text', 'keyboard',))
@telegram_bot.decorators.check_data_for_telegram_bot_command
def add_telegram_bot_command(request: WSGIRequest, telegram_bot: TelegramBot, name: str, command: str, callback: str, message_text: str, keyboard: str) -> HttpResponse:
	TelegramBotCommand.objects.add_telegram_bot_command(
		telegram_bot=telegram_bot,
		name=name,
		command=command,
		callback=callback,
		message_text=message_text,
		keyboard=keyboard
	)

	return HttpResponse('Вы успешно добавили команду Telegram боту.')

@django.views.decorators.csrf.csrf_exempt
@django.contrib.auth.decorators.login_required
@telegram_bot.decorators.check_telegram_bot_id
@telegram_bot.decorators.check_telegram_bot_command_id
def get_telegram_bot_command_data(request: WSGIRequest, telegram_bot: TelegramBot, telegram_bot_command: TelegramBotCommand) -> HttpResponse:
	return HttpResponse(
		json.dumps(
			{
				'name': telegram_bot_command.name,
				'command': telegram_bot_command.command,
				'callback': telegram_bot_command.callback,
				'message_text': telegram_bot_command.message_text,
				'keyboard': telegram_bot_command.keyboard,
			}
		)
	)

@django.views.decorators.csrf.csrf_exempt
@django.contrib.auth.decorators.login_required
@telegram_bot.decorators.check_telegram_bot_id
@telegram_bot.decorators.check_telegram_bot_command_id
@constructor_telegram_bots.decorators.check_post_request_data_items(request_need_items=('name', 'command', 'callback', 'message_text', 'keyboard',))
@telegram_bot.decorators.check_data_for_telegram_bot_command
def edit_telegram_bot_command(request: WSGIRequest, telegram_bot: TelegramBot, telegram_bot_command: TelegramBotCommand, name: str, command: str, callback: str, message_text: str, keyboard: str) -> HttpResponse:
	telegram_bot_command.name = name
	telegram_bot_command.command = command
	telegram_bot_command.callback = callback
	telegram_bot_command.message_text = message_text
	telegram_bot_command.keyboard = keyboard
	telegram_bot_command.save()

	return HttpResponse('Вы успешно изменили команду Telegram бота.')

@django.views.decorators.csrf.csrf_exempt
@django.contrib.auth.decorators.login_required
@telegram_bot.decorators.check_telegram_bot_id
@telegram_bot.decorators.check_telegram_bot_command_id
def delete_telegram_bot_command(request: WSGIRequest, telegram_bot: TelegramBot, telegram_bot_command: TelegramBotCommand) -> HttpResponse:
	telegram_bot_command.delete()

	return HttpResponse('Вы успешно удалили команду Telegram бота.')


@django.views.decorators.csrf.csrf_exempt
@django.contrib.auth.decorators.login_required
@telegram_bot.decorators.check_telegram_bot_id
@telegram_bot.decorators.check_telegram_bot_user_id
def add_allowed_user(request: WSGIRequest, telegram_bot: TelegramBot, telegram_bot_user: TelegramBotUser) -> HttpResponse:
	telegram_bot_user.is_allowed = True
	telegram_bot_user.save()

	return HttpResponse('Вы успешно добавили пользователя в список разрешённых пользователей Telegram бота.')

@django.views.decorators.csrf.csrf_exempt
@django.contrib.auth.decorators.login_required
@telegram_bot.decorators.check_telegram_bot_id
@telegram_bot.decorators.check_telegram_bot_user_id
def delete_allowed_user(request: WSGIRequest, telegram_bot: TelegramBot, telegram_bot_user: TelegramBotUser) -> HttpResponse:
	telegram_bot_user.is_allowed = False
	telegram_bot_user.save()

	return HttpResponse('Вы успешно удалили пользователя из списка разрешённых пользователей Telegram бота.')

@django.views.decorators.csrf.csrf_exempt
@django.contrib.auth.decorators.login_required
@telegram_bot.decorators.check_telegram_bot_id
@telegram_bot.decorators.check_telegram_bot_user_id
def delete_telegram_bot_user(request: WSGIRequest, telegram_bot: TelegramBot, telegram_bot_user: TelegramBotUser) -> HttpResponse:
	telegram_bot_user.delete()

	return HttpResponse('Вы успешно удалили пользователя Telegram бота.')


@django.views.decorators.csrf.csrf_exempt
@django.contrib.auth.decorators.login_required
@telegram_bot.decorators.check_telegram_bot_id
def get_telegram_bot_commands(request: WSGIRequest, telegram_bot: TelegramBot) -> HttpResponse:
	telegram_bot_commands = {'commands_count': telegram_bot.commands.count()}
	for telegram_bot_command in telegram_bot.commands.all():
		telegram_bot_commands.update({telegram_bot_command.id: telegram_bot_command.name})

	return HttpResponse(json.dumps(telegram_bot_commands))

@django.views.decorators.csrf.csrf_exempt
@django.contrib.auth.decorators.login_required
@telegram_bot.decorators.check_telegram_bot_id
def get_telegram_bot_users(request: WSGIRequest, telegram_bot: TelegramBot) -> HttpResponse:
	telegram_bot_users = {'users_count': telegram_bot.users.count()}
	for telegram_bot_user in telegram_bot.users.all():
		telegram_bot_users.update(
			{
				telegram_bot_user.id: {
					'username': telegram_bot_user.username,
					'is_allowed': telegram_bot_user.is_allowed,
					'date_started': telegram_bot_user.date_started.strftime('%d %B %Y г. %H:%M'),
				},
			}
		)

	return HttpResponse(json.dumps(telegram_bot_users))