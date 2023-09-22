from django.utils.translation import gettext as _
from django.conf import settings

from rest_framework.views import APIView
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.status import *

from .models import *
from .services import tasks, database_telegram_bot
from .decorators import *
from .functions import *
from .serializers import *

from typing import Optional
import json
import sys


class TelegramBotsView(APIView):
	authentication_classes = [TokenAuthentication]
	permission_classes = [IsAuthenticated]

	def post(self, request: Request) -> Response:
		serializer = CreateTelegramBotSerializer(data=request.data, context={'user': request.user})
		serializer.is_valid(raise_exception=True)

		validated_data: dict = serializer.validated_data

		telegram_bot: TelegramBot = TelegramBot.objects.create(
			owner=request.user,
			api_token=validated_data['api_token'],
			is_private=validated_data['is_private']
		)

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

	@check_telegram_bot_id
	def patch(self, request: Request, telegram_bot: TelegramBot) -> Response:
		serializer = UpdateTelegramBotSerializer(data=request.data, context={'user': request.user})
		serializer.is_valid(raise_exception=True)

		validated_data: dict = serializer.validated_data
		api_token: Optional[str] = validated_data['api_token']
		is_private: Optional[bool] = validated_data['is_private']

		if api_token is not None:
			username: str = check_telegram_bot_api_token(api_token)

			telegram_bot.username = username
			telegram_bot.api_token = api_token
			telegram_bot.is_running = False
			telegram_bot.save()

			return Response({
				'message': _('Вы успешно изменили API-токен Telegram бота.'),
				'level': 'success',
			})
		elif is_private is not None:
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
		else:
			return Response({
				'message': _('На стороне сайта произошла непредвиденная ошибка, попробуйте ещё раз позже!'),
				'level': 'danger',
			}, status=HTTP_500_INTERNAL_SERVER_ERROR)

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
	if not settings.TEST:
		if not telegram_bot.is_running and telegram_bot.is_stopped:
			if sys.platform == 'win32':
				tasks.start_telegram_bot(telegram_bot_id=telegram_bot.id)
			else:
				tasks.start_telegram_bot.delay(telegram_bot_id=telegram_bot.id)
		elif telegram_bot.is_running and not telegram_bot.is_stopped:
			if sys.platform == 'win32':
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
def update_telegram_bot_diagram_current_scale(request: Request, telegram_bot: TelegramBot) -> Response:
	serializer = UpdateTelegramBotDiagramCurrentScaleSerializer(data=request.data)
	serializer.is_valid(raise_exception=True)

	telegram_bot.diagram_current_scale = serializer.validated_data['diagram_current_scale']
	telegram_bot.save()

	return Response({
		'message': None,
		'level': 'success',
	})

class TelegramBotCommandsView(APIView):
	authentication_classes = [TokenAuthentication]
	permission_classes = [IsAuthenticated]

	@check_telegram_bot_id
	def post(self, request: Request, telegram_bot: TelegramBot) -> Response:
		request_data: dict = json.loads(request.POST['data']) if 'data' in request.POST else request.data

		serializer = CreateTelegramBotCommandSerializer(data=request_data)
		serializer.is_valid(raise_exception=True)

		TelegramBotCommand.objects.create(
			telegram_bot=telegram_bot,
			image=get_image_from_request(request),
			**serializer.validated_data
		)

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
	def patch(self, request: Request, telegram_bot: TelegramBot, telegram_bot_command: TelegramBotCommand) -> Response:
		request_data: dict = json.loads(request.POST['data']) if 'data' in request.POST else request.data

		serializer = UpdateTelegramBotCommandSerializer(data=request_data)
		serializer.is_valid(raise_exception=True)

		telegram_bot_command.update(
			image=get_image_from_request(request),
			**serializer.validated_data
		)

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
def update_telegram_bot_command_position(request: Request, telegram_bot: TelegramBot, telegram_bot_command: TelegramBotCommand) -> Response:
	serializer = UpdateTelegramBotCommandPositionSerializer(data=request.data)
	serializer.is_valid(raise_exception=True)

	validated_data: dict = serializer.validated_data

	telegram_bot_command.x = validated_data['x']
	telegram_bot_command.y = validated_data['y']
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
	def post(
		self,
		request: Request,
		telegram_bot: TelegramBot,
		telegram_bot_command: TelegramBotCommand,
		telegram_bot_command_keyboard_button: TelegramBotCommandKeyboardButton,
	) -> Response:
		serializer = UpdateTelegramBotCommandKeyboardButtonTelegramBotCommandSerializer(data=request.data, context={'telegram_bot': telegram_bot})
		serializer.is_valid(raise_exception=True)

		validated_data: dict = serializer.validated_data

		telegram_bot_command_keyboard_button.telegram_bot_command = telegram_bot.commands.get(id=validated_data['telegram_bot_command_id'])
		telegram_bot_command_keyboard_button.start_diagram_connector = validated_data['start_diagram_connector']
		telegram_bot_command_keyboard_button.end_diagram_connector = validated_data['end_diagram_connector']
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
	def post(self, request: Request, telegram_bot: TelegramBot) -> Response:
		serializer = CreateTelegramBotDatabeseRecordSerializer(data=request.data)
		serializer.is_valid(raise_exception=True)

		record: dict = database_telegram_bot.insert_record(telegram_bot, serializer.validated_data['record'])

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
	def patch(self, request: Request, telegram_bot: TelegramBot, record_id: int) -> Response:
		serializer = UpdateTelegramBotDatabeseRecordSerializer(data=request.data)
		serializer.is_valid(raise_exception=True)

		record: dict = database_telegram_bot.update_record(telegram_bot, record_id, serializer.validated_data['record'])

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
