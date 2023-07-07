from django.core.files.uploadedfile import InMemoryUploadedFile
from django.http import HttpRequest, JsonResponse
from django.utils.translation import gettext as _

from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response

from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from constructor_telegram_bots.decorators import check_post_request_data_items
from telegram_bot.decorators import (
	check_telegram_bot_api_token,
	check_telegram_bot_id,
	check_data_for_telegram_bot_command,
	check_telegram_bot_command_id,
	check_telegram_bot_command_keyboard_button_id,
	check_telegram_bot_user_id
)

from telegram_bot.models import (
	TelegramBot,
	TelegramBotCommand,
	TelegramBotCommandKeyboardButton,
	TelegramBotUser
)

from telegram_bot.services import tasks
from telegram_bot.functions import check_telegram_bot_api_token as check_telegram_bot_api_token_
from telegram_bot.services import database_telegram_bot

from typing import Union
from sys import platform


@csrf_exempt
@require_POST
@login_required
@check_post_request_data_items({'api_token': str, 'is_private': bool})
@check_telegram_bot_api_token
def add_telegram_bot(request: HttpRequest, api_token: str, is_private: bool) -> JsonResponse:
	TelegramBot.objects.create(owner=request.user, api_token=api_token, is_private=is_private)

	return JsonResponse(
		{
			'message': _('Вы успешно добавили Telegram бота.'),
			'level': 'success',
		}
	)

@csrf_exempt
@require_POST
@login_required
@check_telegram_bot_id
@check_post_request_data_items({'api_token': str})
@check_telegram_bot_api_token
def edit_telegram_bot_api_token(request: HttpRequest, telegram_bot: TelegramBot, api_token: bool) -> JsonResponse:
	username: str = check_telegram_bot_api_token_(api_token=api_token)

	telegram_bot.username = username
	telegram_bot.api_token = api_token
	telegram_bot.is_running = False
	telegram_bot.save()

	return JsonResponse(
		{
			'message': _('Вы успешно изменили API-токен Telegram бота.'),
			'level': 'success',
		}
	)

@csrf_exempt
@require_POST
@login_required
@check_telegram_bot_id
@check_post_request_data_items({'is_private': bool})
def edit_telegram_bot_private(request: HttpRequest, telegram_bot: TelegramBot, is_private: bool) -> JsonResponse:
	telegram_bot.is_private = is_private
	telegram_bot.save()

	if is_private:
		return JsonResponse(
			{
				'message': _('Вы успешно сделали Telegram бота приватным.'),
				'level': 'success',
			}
		)
	else:
		return JsonResponse(
			{
				'message': _('Вы успешно сделали Telegram бота не приватным.'),
				'level': 'success',
			}
		)

@csrf_exempt
@require_POST
@login_required
@check_telegram_bot_id
def delete_telegram_bot(request: HttpRequest, telegram_bot: TelegramBot) -> JsonResponse:
	telegram_bot.delete()

	return JsonResponse(
		{
			'message': _('Вы успешно удалили Telegram бота.'),
			'level': 'success',
		}
	)


@csrf_exempt
@require_POST
@login_required
@check_telegram_bot_id
def get_telegram_bot_data(request: HttpRequest, telegram_bot: TelegramBot) -> JsonResponse:
	return JsonResponse(telegram_bot.to_dict())


@csrf_exempt
@require_POST
@login_required
@check_telegram_bot_id
def start_telegram_bot(request: HttpRequest, telegram_bot: TelegramBot) -> JsonResponse:
	if platform == 'win32':
		tasks.start_telegram_bot(telegram_bot_id=telegram_bot.id)
	else:
		tasks.start_telegram_bot.delay(telegram_bot_id=telegram_bot.id)

	return JsonResponse(
		{
			'message': None,
			'level': 'success',
		}
	)

@csrf_exempt
@require_POST
@login_required
@check_telegram_bot_id
def stop_telegram_bot(request: HttpRequest, telegram_bot: TelegramBot) -> JsonResponse:
	if platform == 'win32':
		tasks.stop_telegram_bot(telegram_bot_id=telegram_bot.id)
	else:
		tasks.stop_telegram_bot.delay(telegram_bot_id=telegram_bot.id)

	return JsonResponse(
		{
			'message': None,
			'level': 'success',
		}
	)


@csrf_exempt
@require_POST
@login_required
@check_telegram_bot_id
@check_post_request_data_items(
	{
		'name': str,
		'message_text': str,
		'command': Union[str, None],
		'keyboard': Union[dict, None],
		'api_request': Union[dict, None],
		'database_record': Union[str, None],
	}
)
@check_data_for_telegram_bot_command
def add_telegram_bot_command(
	request: HttpRequest,
	telegram_bot: TelegramBot,
	name: str,
	message_text: str,
	command: Union[str, None] = None,
	image: Union[InMemoryUploadedFile, None] = None,
	keyboard: Union[dict, None] = None,
	api_request: Union[dict, None] = None,
	database_record: Union[str, None] = None,
) -> JsonResponse:
	TelegramBotCommand.objects.create(
		telegram_bot=telegram_bot,
		name=name,
		command=command,
		image=image,
		message_text=message_text,
		keyboard=keyboard,
		api_request=api_request,
		database_record=database_record
	)

	return JsonResponse(
		{
			'message': _('Вы успешно добавили команду Telegram боту.'),
			'level': 'success',
		}
	)

@csrf_exempt
@require_POST
@login_required
@check_telegram_bot_id
@check_telegram_bot_command_id
@check_post_request_data_items(
	{
		'name': str,
		'message_text': str,
		'command': Union[str, None],
		'keyboard': Union[dict, None],
		'api_request': Union[dict, None],
		'database_record': Union[str, None],
	}
)
@check_data_for_telegram_bot_command
def edit_telegram_bot_command(
	request: HttpRequest,
	telegram_bot: TelegramBot,
	telegram_bot_command: TelegramBotCommand,
	name: str,
	message_text: str,
	command: Union[str, None] = None,
	image: Union[InMemoryUploadedFile, str, None] = None,
	keyboard: Union[dict, None] = None,
	api_request: Union[dict, None] = None,
	database_record: Union[str, None] = None,
) -> JsonResponse:
	telegram_bot_command.update(
		telegram_bot_command=telegram_bot_command,
		name=name,
		command=command,
		image=image,
		message_text=message_text,
		keyboard=keyboard,
		api_request=api_request,
		database_record=database_record
	)

	return JsonResponse(
		{
			'message': _('Вы успешно изменили команду Telegram бота.'),
			'level': 'success',
		}
	)

@csrf_exempt
@require_POST
@login_required
@check_telegram_bot_id
@check_telegram_bot_command_id
def delete_telegram_bot_command(request: HttpRequest, telegram_bot: TelegramBot, telegram_bot_command: TelegramBotCommand) -> JsonResponse:
	telegram_bot_command.delete()

	return JsonResponse(
		{
			'message': _('Вы успешно удалили команду Telegram бота.'),
			'level': 'success',
		}
	)


@csrf_exempt
@require_POST
@login_required
@check_telegram_bot_id
@check_telegram_bot_command_id
def get_telegram_bot_command_data(request: HttpRequest, telegram_bot: TelegramBot, telegram_bot_command: TelegramBotCommand) -> JsonResponse:
	return JsonResponse(telegram_bot_command.to_dict())


@csrf_exempt
@require_POST
@login_required
@check_telegram_bot_id
@check_telegram_bot_command_id
@check_telegram_bot_command_keyboard_button_id
@check_post_request_data_items(
	{
		'telegram_bot_command_id': int,
		'start_diagram_connector': str,
		'end_diagram_connector': str,
	}
)
def add_telegram_bot_command_keyboard_button_telegram_bot_command(
	request: HttpRequest,
	telegram_bot: TelegramBot,
	telegram_bot_command: TelegramBotCommand,
	telegram_bot_command_keyboard_button: TelegramBotCommandKeyboardButton,
	telegram_bot_command_id: int,
	start_diagram_connector: str,
	end_diagram_connector: str
) -> JsonResponse:
	if not telegram_bot.commands.filter(id=telegram_bot_command_id).exists():
		return JsonResponse(
			{
				'message': _('Команда Telegram бота не найдена!'),
				'level': 'danger',
			},
			status=400
		)

	telegram_bot_command_keyboard_button.telegram_bot_command = telegram_bot.commands.get(id=telegram_bot_command_id)
	telegram_bot_command_keyboard_button.start_diagram_connector = start_diagram_connector
	telegram_bot_command_keyboard_button.end_diagram_connector = end_diagram_connector
	telegram_bot_command_keyboard_button.save()

	return JsonResponse(
		{
			'message': None,
			'level': 'success',
		}
	)

@csrf_exempt
@require_POST
@login_required
@check_telegram_bot_id
@check_telegram_bot_command_id
@check_telegram_bot_command_keyboard_button_id
def delete_telegram_bot_command_keyboard_button_telegram_bot_command(
	request: HttpRequest,
	telegram_bot: TelegramBot,
	telegram_bot_command: TelegramBotCommand,
	telegram_bot_command_keyboard_button: TelegramBotCommandKeyboardButton
) -> JsonResponse:
	telegram_bot_command_keyboard_button.telegram_bot_command = None
	telegram_bot_command_keyboard_button.start_diagram_connector = None
	telegram_bot_command_keyboard_button.end_diagram_connector = None
	telegram_bot_command_keyboard_button.save()

	return JsonResponse(
		{
			'message': None,
			'level': 'success',
		}
	)


@csrf_exempt
@require_POST
@login_required
@check_telegram_bot_id
@check_telegram_bot_user_id
def add_allowed_user(request: HttpRequest, telegram_bot: TelegramBot, telegram_bot_user: TelegramBotUser) -> JsonResponse:
	telegram_bot_user.is_allowed = True
	telegram_bot_user.save()

	return JsonResponse(
		{
			'message': _('Вы успешно добавили пользователя в список разрешённых пользователей Telegram бота.'),
			'level': 'success',
		}
	)

@csrf_exempt
@require_POST
@login_required
@check_telegram_bot_id
@check_telegram_bot_user_id
def delete_allowed_user(request: HttpRequest, telegram_bot: TelegramBot, telegram_bot_user: TelegramBotUser) -> JsonResponse:
	telegram_bot_user.is_allowed = False
	telegram_bot_user.save()

	return JsonResponse(
		{
			'message': _('Вы успешно удалили пользователя из списка разрешённых пользователей Telegram бота.'),
			'level': 'success',
		}
	)

@csrf_exempt
@require_POST
@login_required
@check_telegram_bot_id
@check_telegram_bot_user_id
def delete_telegram_bot_user(request: HttpRequest, telegram_bot: TelegramBot, telegram_bot_user: TelegramBotUser) -> JsonResponse:
	telegram_bot_user.delete()

	return JsonResponse(
		{
			'message': _('Вы успешно удалили пользователя Telegram бота.'),
			'level': 'success',
		}
	)


@csrf_exempt
@require_POST
@login_required
@check_telegram_bot_id
@check_post_request_data_items({'diagram_current_scale': float})
def save_telegram_bot_diagram_current_scale(request: HttpRequest, telegram_bot: TelegramBot, diagram_current_scale: float) -> JsonResponse:
	if 0.1 <= diagram_current_scale <= 2.0:
		telegram_bot.diagram_current_scale = diagram_current_scale
	else:
		telegram_bot.diagram_current_scale = 1.0
	telegram_bot.save()

	return JsonResponse(
		{
			'message': None,
			'level': 'success',
		}
	)

@csrf_exempt
@require_POST
@login_required
@check_telegram_bot_id
@check_telegram_bot_command_id
@check_post_request_data_items({'x': int, 'y': int})
def save_telegram_bot_command_position(
	request: HttpRequest,
	telegram_bot: TelegramBot,
	telegram_bot_command: TelegramBotCommand,
	x: int,
	y: int
) -> JsonResponse:
	telegram_bot_command.x = x
	telegram_bot_command.y = y
	telegram_bot_command.save()

	return JsonResponse(
		{
			'message': None,
			'level': 'success',
		}
	)


@csrf_exempt
@require_POST
@login_required
@check_telegram_bot_id
def get_telegram_bot_commands(request: HttpRequest, telegram_bot: TelegramBot) -> JsonResponse:
	return JsonResponse(telegram_bot.get_commands_as_dict(), safe=False)

@csrf_exempt
@require_POST
@login_required
@check_telegram_bot_id
def get_telegram_bot_users(request: HttpRequest, telegram_bot: TelegramBot) -> JsonResponse:
	return JsonResponse(telegram_bot.get_users_as_dict(), safe=False)


@csrf_exempt
@require_POST
@login_required
@check_telegram_bot_id
def delete_databese_record(request: HttpRequest, telegram_bot: TelegramBot, record_id: int) -> JsonResponse:
	database_telegram_bot.delete_one_record(telegram_bot, record_id)

	return JsonResponse(
		{
			'message': _('Вы успешно удалили запись из базы данных.'),
			'level': 'success',
		}
	)

@csrf_exempt
@require_POST
@login_required
@check_telegram_bot_id
def get_databese_records(request: HttpRequest, telegram_bot: TelegramBot) -> JsonResponse:
	return JsonResponse(database_telegram_bot.get_all_records(telegram_bot), safe=False)


# def api_delete_databese_record

# class TelegramBotDatabaseView(APIView):
# 	authentication_classes = [SessionAuthentication, TokenAuthentication]
# 	permission_classes = [IsAuthenticated]

# 	@check_telegram_bot_id
# 	def get(self, request: Request, telegram_bot: TelegramBot, format = None) -> Response:
# 		print(request.data)
# 		return Response(database_telegram_bot.get_all_records(telegram_bot))
