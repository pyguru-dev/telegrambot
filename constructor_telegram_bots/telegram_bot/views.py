from django.utils.translation import gettext as _

from rest_framework.views import APIView
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response

from constructor_telegram_bots.decorators import check_post_request_data_items
from .decorators import (
	check_telegram_bot_api_token,
	check_telegram_bot_id,
	check_data_for_telegram_bot_command,
	check_telegram_bot_command_id,
	check_telegram_bot_command_keyboard_button_id,
	check_telegram_bot_user_id
)

from .models import TelegramBot, TelegramBotCommand, TelegramBotCommandKeyboardButton, TelegramBotUser

from .services import tasks, database_telegram_bot
from .functions import check_telegram_bot_api_token as check_telegram_bot_api_token_

from typing import Union
from sys import platform


class TelegramBotsView(APIView):
	authentication_classes = [TokenAuthentication]
	permission_classes = [IsAuthenticated]

	@check_post_request_data_items({'api_token': str, 'is_private': bool})
	@check_telegram_bot_api_token
	def post(self, request: Request, api_token: str, is_private: bool) -> Response:
		telegram_bot: TelegramBot = TelegramBot.objects.create(owner=request.user, api_token=api_token, is_private=is_private)

		return Response({
			'message': _('Вы успешно добавили Telegram бота.'),
			'level': 'success',

			'telegram_bot': telegram_bot.to_dict(),
		})

	def get(self, request: Request) -> Response:
		return Response(request.user.get_telegram_bots_as_dict())

class TelegramBotView(APIView):
	authentication_classes = [TokenAuthentication]
	permission_classes = [IsAuthenticated]

	@check_telegram_bot_api_token
	def edit_telegram_bot_api_token(self, request: Request, telegram_bot: TelegramBot, api_token: bool) -> Response:
		username: str = check_telegram_bot_api_token_(api_token)

		telegram_bot.username = username
		telegram_bot.api_token = api_token
		telegram_bot.is_running = False
		telegram_bot.save()

		return Response({
			'message': _('Вы успешно изменили API-токен Telegram бота.'),
			'level': 'success',
		})

	def edit_telegram_bot_private(self, request: Request, telegram_bot: TelegramBot, is_private: bool) -> Response:
		telegram_bot.is_private = is_private
		telegram_bot.save()

		if is_private:
			return Response({
				'message': _('Вы успешно сделали Telegram бота приватным.'),
				'level': 'success',
			})
		else:
			return Response({
				'message': _('Вы успешно сделали Telegram бота не приватным.'),
				'level': 'success',
			})

	@check_telegram_bot_id
	@check_post_request_data_items({'api_token': Union[str, None], 'is_private': Union[bool, None]})
	def patch(self, request: Request, telegram_bot: TelegramBot, api_token: Union[str, None], is_private: Union[bool, None]) -> Response:
		if api_token is not None:
			return self.edit_telegram_bot_api_token(request, telegram_bot=telegram_bot, api_token=api_token)
		elif is_private is not None:
			return self.edit_telegram_bot_private(request, telegram_bot=telegram_bot, is_private=is_private)
		else:
			return Response({
				'message': _('Произошла ошибка, попробуйте ещё раз позже!'),
				'level': 'danger',
			})

	@check_telegram_bot_id
	def delete(self, request: Request, telegram_bot: TelegramBot) -> Response:
		telegram_bot.delete()

		return Response({
			'message': _('Вы успешно удалили Telegram бота.'),
			'level': 'success',
		})

	@check_telegram_bot_id
	def get(self, request: Request, telegram_bot: TelegramBot) -> Response:
		return Response(telegram_bot.to_dict())

@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
@check_telegram_bot_id
def start_or_stop_telegram_bot(request: Request, telegram_bot: TelegramBot) -> Response:
	if not telegram_bot.is_running and telegram_bot.is_stopped:
		if platform == 'win32':
			tasks.start_telegram_bot(telegram_bot_id=telegram_bot.id)
		else:
			tasks.start_telegram_bot.delay(telegram_bot_id=telegram_bot.id)
	elif telegram_bot.is_running and not telegram_bot.is_stopped:
		if platform == 'win32':
			tasks.stop_telegram_bot(telegram_bot_id=telegram_bot.id)
		else:
			tasks.stop_telegram_bot.delay(telegram_bot_id=telegram_bot.id)

	return Response({
		'message': None,
		'level': 'success',
	})

@api_view(['PATCH'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
@check_telegram_bot_id
@check_post_request_data_items({'diagram_current_scale': Union[int, float]})
def save_telegram_bot_diagram_current_scale(request: Request, telegram_bot: TelegramBot, diagram_current_scale: float) -> Response:
	if 0.1 <= diagram_current_scale <= 2.0:
		telegram_bot.diagram_current_scale = diagram_current_scale
	else:
		telegram_bot.diagram_current_scale = 1.0
	telegram_bot.save()

	return Response({
		'message': None,
		'level': 'success',
	})

class TelegramBotCommandsView(APIView):
	authentication_classes = [TokenAuthentication]
	permission_classes = [IsAuthenticated]

	@check_telegram_bot_id
	@check_post_request_data_items({
		'name': str,
		'message_text': str,
		'command': Union[str, None],
		'keyboard': Union[dict, None],
		'api_request': Union[dict, None],
		'database_record': Union[str, None],
	})
	@check_data_for_telegram_bot_command
	def post(self, request: Request, **fields) -> Response:
		TelegramBotCommand.objects.create(**fields)

		return Response({
			'message': _('Вы успешно добавили команду Telegram боту.'),
			'level': 'success',
		})

	@check_telegram_bot_id
	def get(self, request: Request, telegram_bot: TelegramBot) -> Response:
		return Response(telegram_bot.get_commands_as_dict(escape=True))

class TelegramBotCommandView(APIView):
	authentication_classes = [TokenAuthentication]
	permission_classes = [IsAuthenticated]

	@check_telegram_bot_id
	@check_telegram_bot_command_id
	@check_post_request_data_items({
		'name': str,
		'message_text': str,
		'command': Union[str, None],
		'keyboard': Union[dict, None],
		'api_request': Union[dict, None],
		'database_record': Union[str, None],
	})
	@check_data_for_telegram_bot_command
	def patch(self, request: Request, telegram_bot: TelegramBot, telegram_bot_command: TelegramBotCommand, **fields) -> Response:
		telegram_bot_command.update(**fields)

		return Response({
			'message': _('Вы успешно изменили команду Telegram бота.'),
			'level': 'success',
		})

	@check_telegram_bot_id
	@check_telegram_bot_command_id
	def delete(self, request: Request, telegram_bot: TelegramBot, telegram_bot_command: TelegramBotCommand) -> Response:
		telegram_bot_command.delete()

		return Response({
			'message': _('Вы успешно удалили команду Telegram бота.'),
			'level': 'success',
		})

	@check_telegram_bot_id
	@check_telegram_bot_command_id
	def get(self, request: Request, telegram_bot: TelegramBot, telegram_bot_command: TelegramBotCommand) -> Response:
		return Response(telegram_bot_command.to_dict())

@api_view(['PATCH'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
@check_telegram_bot_id
@check_telegram_bot_command_id
@check_post_request_data_items({'x': int, 'y': int})
def save_telegram_bot_command_position(
	request: Request,
	telegram_bot: TelegramBot,
	telegram_bot_command: TelegramBotCommand,
	x: int,
	y: int
) -> Response:
	telegram_bot_command.x = x
	telegram_bot_command.y = y
	telegram_bot_command.save()

	return Response({
		'message': None,
		'level': 'success',
	})

class TelegramBotCommandKeyboardButtonTelegramBotCommandView(APIView):
	authentication_classes = [TokenAuthentication]
	permission_classes = [IsAuthenticated]

	@check_telegram_bot_id
	@check_telegram_bot_command_id
	@check_telegram_bot_command_keyboard_button_id
	@check_post_request_data_items({
		'telegram_bot_command_id': int,
		'start_diagram_connector': str,
		'end_diagram_connector': str,
	})
	def post(
		self,
		request: Request,
		telegram_bot: TelegramBot,
		telegram_bot_command: TelegramBotCommand,
		telegram_bot_command_keyboard_button: TelegramBotCommandKeyboardButton,
		telegram_bot_command_id: int,
		start_diagram_connector: str,
		end_diagram_connector: str
	) -> Response:
		if not telegram_bot.commands.filter(id=telegram_bot_command_id).exists():
			return Response({
				'message': _('Команда Telegram бота не найдена!'),
				'level': 'danger',
			}, status=400)

		telegram_bot_command_keyboard_button.telegram_bot_command = telegram_bot.commands.get(id=telegram_bot_command_id)
		telegram_bot_command_keyboard_button.start_diagram_connector = start_diagram_connector
		telegram_bot_command_keyboard_button.end_diagram_connector = end_diagram_connector
		telegram_bot_command_keyboard_button.save()

		return Response({
			'message': None,
			'level': 'success',
		})

	@check_telegram_bot_id
	@check_telegram_bot_command_id
	@check_telegram_bot_command_keyboard_button_id
	def delete(
		self,
		request: Request,
		telegram_bot: TelegramBot,
		telegram_bot_command: TelegramBotCommand,
		telegram_bot_command_keyboard_button: TelegramBotCommandKeyboardButton
	) -> Response:
		telegram_bot_command_keyboard_button.telegram_bot_command = None
		telegram_bot_command_keyboard_button.start_diagram_connector = None
		telegram_bot_command_keyboard_button.end_diagram_connector = None
		telegram_bot_command_keyboard_button.save()

		return Response({
			'message': None,
			'level': 'success',
		})

class TelegramBotUsersView(APIView):
	authentication_classes = [TokenAuthentication]
	permission_classes = [IsAuthenticated]

	@check_telegram_bot_id
	def get(self, request: Request, telegram_bot: TelegramBot) -> Response:
		return Response(telegram_bot.get_users_as_dict())

class TelegramBotUserView(APIView):
	authentication_classes = [TokenAuthentication]
	permission_classes = [IsAuthenticated]

	@check_telegram_bot_id
	@check_telegram_bot_user_id
	def delete(self, request: Request, telegram_bot: TelegramBot, telegram_bot_user: TelegramBotUser) -> Response:
		telegram_bot_user.delete()

		return Response({
			'message': _('Вы успешно удалили пользователя Telegram бота.'),
			'level': 'success',
		})

class TelegramBotAllowedUserView(APIView):
	authentication_classes = [TokenAuthentication]
	permission_classes = [IsAuthenticated]

	@check_telegram_bot_id
	@check_telegram_bot_user_id
	def post(self, request: Request, telegram_bot: TelegramBot, telegram_bot_user: TelegramBotUser) -> Response:
		telegram_bot_user.is_allowed = True
		telegram_bot_user.save()

		return Response({
			'message': _('Вы успешно добавили пользователя в список разрешённых пользователей Telegram бота.'),
			'level': 'success',
		})

	@check_telegram_bot_id
	@check_telegram_bot_user_id
	def delete(self, request: Request, telegram_bot: TelegramBot, telegram_bot_user: TelegramBotUser) -> Response:
		telegram_bot_user.is_allowed = False
		telegram_bot_user.save()

		return Response({
			'message': _('Вы успешно удалили пользователя из списка разрешённых пользователей Telegram бота.'),
			'level': 'success',
		})

class TelegramBotDatabeseRecordsView(APIView):
	authentication_classes = [TokenAuthentication]
	permission_classes = [IsAuthenticated]

	@check_telegram_bot_id
	@check_post_request_data_items({'record': dict})
	def post(self, request: Request, telegram_bot: TelegramBot, record: dict) -> Response:
		database_telegram_bot.insert_record(telegram_bot, record)

		return Response({
			'message': _('Вы успешно добавили запись в базу данных Telegram бота.'),
			'level': 'success',

			'record': record,
		})

	@check_telegram_bot_id
	def get(self, request: Request, telegram_bot: TelegramBot) -> Response:
		return Response(database_telegram_bot.get_records(telegram_bot))

class TelegramBotDatabeseRecordView(APIView):
	authentication_classes = [TokenAuthentication]
	permission_classes = [IsAuthenticated]

	@check_telegram_bot_id
	@check_post_request_data_items({'updated_record': dict})
	def patch(self, request: Request, telegram_bot: TelegramBot, record_id: int, updated_record: dict) -> Response:
		record: dict = database_telegram_bot.update_record(telegram_bot, record_id, updated_record)

		return Response({
			'message': _('Вы успешно обновили запись в базе данных Telegram бота.'),
			'level': 'success',

			'record': record,
		})

	@check_telegram_bot_id
	def delete(self, request: Request, telegram_bot: TelegramBot, record_id: int) -> Response:
		database_telegram_bot.delete_record(telegram_bot, record_id)

		return Response({
			'message': _('Вы успешно удалили запись из базы данных Telegram бота.'),
			'level': 'success',
		})
