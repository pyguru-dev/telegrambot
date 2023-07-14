from django.utils.translation import gettext as _

from rest_framework.decorators import APIView
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response

from constructor_telegram_bots.decorators import check_post_request_data_items
from telegram_bot.decorators import check_telegram_bot_id
from .decorators import check_plugin_id

from .models import Plugin, PluginLog
from telegram_bot.models import TelegramBot

from constructor_telegram_bots import environment


class PluginsView(APIView):
	authentication_classes = [TokenAuthentication]
	permission_classes = [IsAuthenticated]

	@check_post_request_data_items({'name': str, 'code': str})
	@check_telegram_bot_id
	def post(self, request: Request, telegram_bot: TelegramBot, name: str, code: str) -> Response:
		plugin: Plugin = Plugin.objects.create(user=request.user, telegram_bot=telegram_bot, name=name, code=code)

		environment.add_plugin(plugin)

		return Response({
			'message': _('Вы успешно добавили плагин вашему Telgram боту.'),
			'level': 'success',
		})

	@check_telegram_bot_id
	def get(self, request: Request, telegram_bot: TelegramBot) -> Response:
		return Response([plugin.to_dict() for plugin in telegram_bot.plugins])

class PluginView(APIView):
	authentication_classes = [TokenAuthentication]
	permission_classes = [IsAuthenticated]

	@check_post_request_data_items({'code': str})
	@check_plugin_id
	def patch(self, request: Request, plugin: Plugin, code: str) -> Response:
		plugin.code = code
		plugin.save()

		environment.update_plugin(plugin)

		return Response({
			'message': _('Вы успешно обновили плагин вашего Telgram бота.'),
			'level': 'success',
		})

	@check_plugin_id
	def delete(self, request: Request, plugin: Plugin) -> Response:
		plugin.delete()

		environment.delete_plugin(plugin)

		return Response({
			'message': _('Вы успешно удалили плагин вашего Telgram бота.'),
			'level': 'success',
		})

class PluginLogsView(APIView):
	authentication_classes = [TokenAuthentication]
	permission_classes = [IsAuthenticated]

	@check_post_request_data_items({'message': str, 'level': str})
	@check_plugin_id
	def post(self, request: Request, plugin: Plugin, message: str, level: str) -> Response:
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

	@check_plugin_id
	def get(self, request: Request, plugin: Plugin) -> Response:
		return Response([plugin_log.to_dict() for plugin_log in plugin.logs])
