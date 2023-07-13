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


class Plugins(APIView):
	authentication_classes = [TokenAuthentication]
	permission_classes = [IsAuthenticated]

	@check_post_request_data_items({'telegram_bot_id': int, 'name': str, 'code': str})
	@check_telegram_bot_id
	def post(request: Request, telegram_bot: TelegramBot, name: str, code: str) -> Response:
		plugin: Plugin = Plugin.objects.create(user=request.user, telegram_bot=telegram_bot, name=name, code=code)

		environment.add_plugin(plugin)

		return Response(
			{
				'message': 'Вы успешно добавили плагин вашему Telgram боту.',
				'level': 'success',
			}
		)

	@check_post_request_data_items({'plugin_id': int, 'name': str, 'code': str})
	@check_plugin_id
	def patch(request: Request, telegram_bot: TelegramBot, plugin: Plugin, name: str, code: str) -> Response:
		plugin.code = code
		plugin.save()

		environment.update_plugin(plugin)

		return Response(
			{
				'message': 'Вы успешно обновили плагин вашего Telgram бота.',
				'level': 'success',
			}
		)

	@check_post_request_data_items({'plugin_id': int})
	@check_plugin_id
	def delete(request: Request, telegram_bot: TelegramBot, plugin: Plugin) -> Response:
		plugin.delete()

		environment.delete_plugin(plugin)

		return Response(
			{
				'message': 'Вы успешно удалили плагин вашего Telgram бота.',
				'level': 'success',
			}
		)

class PluginLogs(APIView):
	authentication_classes = [TokenAuthentication]
	permission_classes = [IsAuthenticated]

	@check_post_request_data_items({'plugin_id': int, 'message': str, 'level': str})
	@check_plugin_id
	def post(request: Request, plugin: Plugin, message: str, level: str) -> Response:
		PluginLog.objects.create(
			user=request.user,
			telegram_bot=plugin.telegram_bot,
			plugin=plugin,
			message=message,
			level=level
		)

		return Response()

	@check_post_request_data_items({'plugin_id': int})
	@check_plugin_id
	def get(request: Request, plugin: Plugin) -> Response:
		return Response([plugin_log.to_dict() for plugin_log in plugin.logs])
