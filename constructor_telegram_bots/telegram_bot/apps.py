from django.apps import AppConfig


class TelegramBotConfig(AppConfig):
	default_auto_field = 'django.db.models.BigAutoField'
	name = 'telegram_bot'

	def ready(self) -> None:
		from telegram_bots.tasks import start_all_telegram_bots

		start_all_telegram_bots.delay()

		return super().ready()
