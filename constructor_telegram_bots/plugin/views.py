from django.utils.translation import gettext as _

from rest_framework.decorators import APIView, api_view, authentication_classes, permission_classes
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response

from constructor_telegram_bots.decorators import check_post_request_data_items

from telegram_bot.models import TelegramBot
from telegram_bot.decorators import check_telegram_bot_id

from .models import *
from .decorators import check_plugin_id, check_plugin_data

from constructor_telegram_bots import environment


class PluginsView(APIView):
	authentication_classes = [TokenAuthentication]
	permission_classes = [IsAuthenticated]

	@check_telegram_bot_id
	@check_post_request_data_items({'name': str, 'code': str})
	@check_plugin_data
	def post(self, request: Request, telegram_bot: TelegramBot, name: str, code: str) -> Response:
		plugin: Plugin = Plugin.objects.create(
			user=request.user,
			telegram_bot=telegram_bot,
			name=name,
			code=code
		)

		return Response({
			'message': _('Вы успешно добавили плагин вашему Telegram боту.'),
			'level': 'success',

			'plugin': plugin.to_dict(),
		})

	@check_telegram_bot_id
	def get(self, request: Request, telegram_bot: TelegramBot) -> Response:
		return Response([plugin.to_dict() for plugin in telegram_bot.plugins.all()])

class PluginView(APIView):
	authentication_classes = [TokenAuthentication]
	permission_classes = [IsAuthenticated]

	@check_plugin_id
	@check_post_request_data_items({'code': str})
	@check_plugin_data
	def patch(self, request: Request, plugin: Plugin, code: str) -> Response:
		plugin.is_checked = False
		plugin.code = code
		plugin.save()

		environment.delete_plugin(plugin)

		return Response({
			'message': _('Вы успешно обновили плагин вашего Telegram бота.'),
			'level': 'success',

			'plugin': plugin.to_dict(),
		})

	@check_plugin_id
	def delete(self, request: Request, plugin: Plugin) -> Response:
		plugin.delete()

		return Response({
			'message': _('Вы успешно удалили плагин вашего Telegram бота.'),
			'level': 'success',
		})

@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
@check_telegram_bot_id
def get_plugins_logs_view(request: Request, telegram_bot: TelegramBot) -> Response:
	return Response([plugin_log.to_dict() for plugin in telegram_bot.plugins.all() for plugin_log in plugin.logs.all()])

@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
@check_plugin_id
@check_post_request_data_items({'message': str, 'level': str})
def add_plugin_log_view(request: Request, plugin: Plugin, message: str, level: str) -> Response:
	PluginLog.objects.create(
		user=request.user,
		telegram_bot=plugin.telegram_bot,
		plugin=plugin,
		message=message,
		level=level
	)

	return Response({
		'message': None,
		'level': 'success',
	})
